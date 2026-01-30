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
        """Get connection parameters with keepalive settings."""
        return {
            'dsn': settings.DATABASE_URL,
            # TCP keepalive settings to detect dead connections
            'keepalives': 1,
            'keepalives_idle': 30,      # Start keepalive after 30s idle
            'keepalives_interval': 10,  # Send keepalive every 10s
            'keepalives_count': 5,      # Close after 5 failed keepalives
            'connect_timeout': 10,      # Connection timeout
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
        """Test if connection is still alive."""
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
        
        # Test if connection is still valid
        if not cls._test_connection(conn):
            logger.warning("Stale connection detected, reconnecting...")
            try:
                conn.close()
            except Exception:
                pass
            # Put back the dead connection and get a fresh one
            cls._pool.putconn(conn, close=True)
            conn = cls._pool.getconn()
            
            # Verify the new connection works
            if not cls._test_connection(conn):
                raise Exception("Failed to establish database connection")
        
        try:
            yield conn
        finally:
            # Return connection, closing if broken
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
