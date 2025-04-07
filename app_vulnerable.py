import mysql.connector
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'mysql'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'security_demo')
    )

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Demo (Vulnerable Version)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        input, button { padding: 8px; margin: 5px 0; }
        .result { margin-top: 20px; padding: 10px; background-color: #f0f0f0; }
        .vulnerable-badge { background-color: red; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Login <span class="vulnerable-badge">Vulnerable</span></h1>
        <p>This version is intentionally vulnerable to SQL injection for testing purposes.</p>
        <form method="POST">
            <div>
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div>
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        
        {% if error %}
        <div class="result" style="color: red;">
            {{ error }}
        </div>
        {% endif %}
        
        {% if user_info %}
        <div class="result">
            <h2>User Information:</h2>
            <pre>{{ user_info }}</pre>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    user_info = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Basic input validation
        if not username or not password:
            error = "Username and password are required"
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # VULNERABLE QUERY — DO NOT DO THIS IN REAL LIFE!
            query = f"""
                SELECT t1.userid, t1.firstname, t1.lastname, t1.ssn, t1.history 
                FROM user_data t1 
                JOIN user_auth t2 ON t1.userid = t2.userid 
                WHERE t2.username = '{username}' AND t2.pass = '{password}'
            """
            
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                
                if result:
                    user_info = ""
                    for row in result:
                        for key, value in row.items():
                            user_info += f"{key}: {value}\n"
                else:
                    error = "Invalid username or password"
                    
            except mysql.connector.Error as e:
                error = f"Database error: {str(e)}"
            finally:
                cursor.close()
                conn.close()
    
    return render_template_string(HTML_TEMPLATE, error=error, user_info=user_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
