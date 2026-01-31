import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from psycopg2 import OperationalError
from contextlib import contextmanager
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    _pool = None

    @classmethod
    def _get_connection_kwargs(cls):
        """get conection params with keepalive setings"""
        return {
            'dsn': settings.DATABASE_URL,
            # tcp keepalive setings to detect dead conections
            'keepalives': 1,
            'keepalives_idle': 30,      # start keepalive after 30s of idel
            'keepalives_interval': 10,  # send keepalive evry 10s
            'keepalives_count': 5,      # close conection after 5 failed keepalives
            'connect_timeout': 10,      # conection timeout
        }

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            kwargs = cls._get_connection_kwargs()
            cls._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                **kwargs
            )
            logger.info("Database connection pool created successfully")

    @classmethod
    def _test_connection(cls, conn):
        """test if conection still works"""
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except (OperationalError, psycopg2.InterfaceError):
            return False

    @classmethod
    @contextmanager
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize()

        conn = cls._pool.getconn()
        
        # test if conection is still valid
        if not cls._test_connection(conn):
            logger.warning("Stale connection detected, reconnecting...")
            try:
                conn.close()
            except Exception:
                pass
            # put back dead conection and get new one
            cls._pool.putconn(conn, close=True)
            conn = cls._pool.getconn()
            
            # make sure new conection works
            if not cls._test_connection(conn):
                raise Exception("Failed to establish database connection")
        
        try:
            yield conn
        finally:
            # return conection, close if its broken
            try:
                if conn.closed:
                    cls._pool.putconn(conn, close=True)
                else:
                    cls._pool.putconn(conn)
            except Exception as e:
                logger.warning(f"Error returning connection to pool: {e}")
                try:
                    cls._pool.putconn(conn, close=True)
                except Exception:
                    pass

    @classmethod
    @contextmanager
    def get_cursor(cls, commit=False):
        with cls.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

db = Database()
