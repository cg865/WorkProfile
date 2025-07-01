import requests
import time
import sys
import os

NGINX_URL = os.environ.get("NGINX_URL", "http://localhost:8080")


def get(path="/", timeout=10):
    """Send a GET request to NGINX"""
    return requests.get(f"{NGINX_URL}{path}", timeout=timeout)


def wait_for_stack(max_retries=60, delay=2):
    """Wait for the complete 3-tier stack to be ready  (nginx → app → db)"""
    print("Waiting for 3-tier stack (nginx -> app -> database) to be ready...")

    for attempt in range(max_retries):
        try:
            # Test nginx endpoint
            response = get("/health")
            if response.status_code == 200 and "Database: Healthy" in response.text:
                print(f"✓ 3-tier stack ready after {attempt * delay} seconds")
                return True
        except requests.RequestException:
            pass

        print(f"Attempt {attempt + 1}/{max_retries} - waiting {delay} seconds...")
        time.sleep(delay)

    print("✗ 3-tier stack did not become ready in time")
    return False


def test_nginx_proxy():
    """Test that nginx is properly proxying to the application"""
    print("🔎 Testing NGINX reverse proxy...")
    try:
        response = get("/")
        assert (
            response.status_code == 200
        ), f"Nginx proxy failed: {response.status_code}"
        print("✓ Nginx reverse proxy test passed")
        return True
    except Exception as e:
        print(f"✗ Nginx reverse proxy test failed: {e}")
        return False


def test_health_endpoint():
    """Test health endpoint through nginx"""
    print("🔎 Testing /health endpoint...")
    try:
        response = get("/health")
        assert (
            response.status_code == 200
        ), f"Health check failed: {response.status_code}"
        health_text = response.text
        assert (
            "Database: Healthy" in health_text
        ), f"Database not healthy: {health_text}"
        assert (
            "Application: Healthy" in health_text
        ), f"Application not healthy: {health_text}"

        print("✓ Health endpoint test passed")
        print(f"  Health status: {health_text}")
        return True
    except Exception as e:
        print(f"✗ Health endpoint test failed: {e}")
        return False


def test_main_page():
    """Test main page loads through nginx"""
    print("🔎 Testing main page...")
    try:
        response = get("/")
        assert response.status_code == 200, f"Main page failed: {response.status_code}"

        # Check for basic page content
        page_content = response.text.lower()
        assert (
            "workprofile" in page_content or "people" in page_content
        ), "Main page content not found"

        print("✓ Main page test passed")
        return True
    except Exception as e:
        print(f"✗ Main page test failed: {e}")
        return False


def test_3tier_architecture():
    """Test that 3-tier architecture is working"""
    print("🔎 Testing 3-tier architecture...")
    try:
        # This tests nginx -> app -> database connectivity
        response = get("/health")
        assert response.status_code == 200, "3-tier connectivity failed"

        health_text = response.text
        # If database is healthy, it means: nginx -> app -> mysql all working
        assert "Database: Healthy" in health_text, "3-tier database connectivity failed"

        print("✓ 3-tier architecture test passed (nginx -> app -> mysql)")
        return True
    except Exception as e:
        print(f"✗ 3-tier architecture test failed: {e}")
        return False


def run_all_tests():
    """Run all simplified E2E tests"""
    print("=== Starting Simplified E2E Tests ===")
    print("Testing 3-tier architecture: nginx -> WorkProfile -> MySQL")

    # Wait for complete stack
    if not wait_for_stack():
        print("✗ Stack readiness check failed")
        sys.exit(1)

    tests = [
        test_nginx_proxy,
        test_health_endpoint,
        test_main_page,
        test_3tier_architecture,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print("\n=== E2E Test Results ===")
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("✓ All simplified E2E tests passed!")
        print("✓ 3-tier architecture (nginx -> app -> database) working correctly!")
        sys.exit(0)
    else:
        print("✗ Some E2E tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
