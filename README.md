# SQL Injection Demo

This project demonstrates SQL injection vulnerabilities for educational purposes (CSC435 - Computer Security homework). It includes both a vulnerable and a secure version of a web application written in Flask and backed by MySQL.

---

## 🐳 Setup Instructions

> Requires Docker + Docker Compose

### 1. Clone the repository and navigate to it

```bash
git clone <your-repo-url>
cd cybersec-project
```

### 2. Build and run the **vulnerable app** (port `8080`)

```bash
docker compose -p vulnerable_app -f docker-compose.yml build
docker compose -p vulnerable_app -f docker-compose.yml up
```

Then open in your browser:

```
http://localhost:8080
```

### 3. Build and run the **secure app** (port `8081`) — in a new terminal

```bash
docker compose -p secure_app -f docker-compose.secure.yml build
docker compose -p secure_app -f docker-compose.secure.yml up
```

Then open in your browser:

```
http://localhost:8081
```

### 4. Run SQL Injection Tests

Once both apps are running:

```bash
python3 test_sql_injection.py
```

---

## 👤 Sample Users

The following users are pre-configured in the database:

| Username | Password    |
| -------- | ----------- |
| johnd    | password123 |
| janes    | smith2022   |
| admin    | admin123    |
| bobj     | support2023 |

---

## 💥 Demonstrating SQL Injection (Vulnerable App)

This application is intentionally vulnerable to SQL injection. Try the following attacks in the **vulnerable app** (http://localhost:8080):

### 1. 🔓 Bypass Authentication

```text
Username: admin' --
Password: anything
```

Alternative:

```text
Username: admin'#
Password: anything
```

### 2. 📋 Display All Users

```text
Username: ' OR '1'='1
Password: ' OR '1'='1
```

### 3. 🧪 Union-Based Data Extraction

```text
Username: ' UNION SELECT 1,2,3,4,5 --
Password: anything
```

Alternative:

```text
Username: ' UNION SELECT 1,2,3,4,5#
Password: anything
```

---

## 🔐 Secure Version

The secure app on port 8081 uses parameterized queries to prevent SQL injection. All the attacks above should **fail** when run against `http://localhost:8081`.

---

## 🧹 Clean Up

To stop and remove everything:

```bash
docker compose -p vulnerable_app -f docker-compose.yml down -v
docker compose -p secure_app -f docker-compose.secure.yml down -v
```

---

## 📚 References

- https://unixwiz.net/techtips/sql-injection.html
- https://owasp.org/www-community/attacks/SQL_Injection

---

## 🧠 Notes

- Make sure ports 8080 and 8081 are not in use before launching.
- Use two terminals: one for the vulnerable app, one for the secure app.
- The test script `test_sql_injection.py` compares both automatically.
