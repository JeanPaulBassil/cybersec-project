import requests
import time
import sys

# Colors for terminal output


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_failure(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.ENDC}")


def test_login(url, username, password, expected_success, attack_type=""):
    print_info(f"Testing: {attack_type if attack_type else 'Normal login'}")
    print(f"  URL: {url}")
    print(f"  Username: {username}")
    print(f"  Password: {password}")

    try:
        response = requests.post(
            url, data={"username": username, "password": password})

        # Check if login was successful (assume success if we see user information)
        is_successful = "User Information" in response.text

        if is_successful == expected_success:
            if attack_type:
                if expected_success:
                    print_success(f"SQL Injection successful: {attack_type}")
                else:
                    print_success(f"Attack prevented: {attack_type}")
            else:
                print_success("Normal login behaved as expected")
        else:
            if attack_type:
                if expected_success:
                    print_failure(f"SQL Injection failed: {attack_type}")
                else:
                    print_failure(
                        f"SECURITY RISK: Attack succeeded when it should have been prevented: {attack_type}")
            else:
                print_failure("Normal login did not behave as expected")

        # Print response details
        print("  Response content:")
        for line in response.text.split("\n"):
            if "User Information" in line or "userid" in line or "ssn" in line:
                print(f"    {line.strip()}")

        print("  " + "-" * 40)
        return is_successful

    except requests.RequestException as e:
        print_failure(f"Request failed: {e}")
        return False


def main():
    vulnerable_url = "http://localhost:8080/"
    secure_url = "http://localhost:8081/"

    # Test URLs to see if services are running
    try:
        vulnerable_response = requests.get(vulnerable_url)
        print_success("Vulnerable app is running")
    except requests.RequestException:
        print_failure(f"Vulnerable app is not accessible at {vulnerable_url}")
        print_info("Make sure docker-compose up is running")
        return

    try:
        secure_response = requests.get(secure_url)
        print_success("Secure app is running")
    except requests.RequestException:
        print_failure(f"Secure app is not accessible at {secure_url}")
        print_info(
            "Make sure docker-compose -f docker-compose.secure.yml up is running")
        return

    # Test cases to run
    tests = [
        # Normal login tests
        {"username": "johnd", "password": "password123",
            "expected": True, "attack_type": ""},
        {"username": "wronguser", "password": "wrongpass",
            "expected": False, "attack_type": ""},

        # SQL Injection attacks
        {"username": "admin' -- ", "password": "anything", "expected": True,
            "attack_type": "Authentication bypass with -- comment"},
        {"username": "admin'#", "password": "anything", "expected": True,
            "attack_type": "Authentication bypass with # comment"},
        {"username": "' OR '1'='1", "password": "' OR '1'='1",
            "expected": True, "attack_type": "OR condition to return all rows"},
        {"username": "' UNION SELECT 1,2,3,4,5 -- ", "password": "anything",
            "expected": True, "attack_type": "UNION attack to extract data"}
    ]

    # Test vulnerable app
    print_header("TESTING VULNERABLE APP")
    print_info("These attacks should succeed on the vulnerable app")
    for test in tests:
        test_login(vulnerable_url, test["username"],
                   test["password"], test["expected"], test["attack_type"])
        time.sleep(0.5)  # Small delay between requests

    # Test secure app
    print_header("TESTING SECURE APP")
    print_info("The same attacks should fail on the secure app")
    for test in tests:
        # For secure app, SQL injection attacks should fail
        expected = test["expected"] if not test["attack_type"] else False
        test_login(secure_url, test["username"],
                   test["password"], expected, test["attack_type"])
        time.sleep(0.5)  # Small delay between requests


if __name__ == "__main__":
    main()
