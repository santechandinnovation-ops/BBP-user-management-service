import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register_success():
    print("\n=== Testing Registration (Success) ===")
    data = {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_register_duplicate():
    print("\n=== Testing Registration (Duplicate Email) ===")
    data = {
        "username": "janedoe",
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 409

def test_register_weak_password():
    print("\n=== Testing Registration (Weak Password) ===")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "weak"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 422

def test_login_success():
    print("\n=== Testing Login (Success) ===")
    data = {
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if response.status_code == 200:
        return result.get("token")
    return None

def test_login_wrong_password():
    print("\n=== Testing Login (Wrong Password) ===")
    data = {
        "email": "john.doe@example.com",
        "password": "WrongPassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 401

def test_get_profile(token):
    print("\n=== Testing Get Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_profile_no_token():
    print("\n=== Testing Get Profile (No Token) ===")
    response = requests.get(f"{BASE_URL}/users/profile")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 401

def test_logout(token):
    print("\n=== Testing Logout ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    print("=" * 60)
    print("Starting User Management Service Tests")
    print("=" * 60)

    results = []

    results.append(("Health Check", test_health()))
    results.append(("Register Success", test_register_success()))
    results.append(("Register Duplicate", test_register_duplicate()))
    results.append(("Register Weak Password", test_register_weak_password()))

    token = test_login_success()
    results.append(("Login Success", token is not None))

    results.append(("Login Wrong Password", test_login_wrong_password()))

    if token:
        results.append(("Get Profile", test_get_profile(token)))
        results.append(("Logout", test_logout(token)))

    results.append(("Get Profile No Token", test_get_profile_no_token()))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<40} {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    run_all_tests()
