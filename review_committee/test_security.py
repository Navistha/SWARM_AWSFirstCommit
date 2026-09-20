from review_agents.security_reviewer import build_security_agent
from review_agents.base import review

VULNERABLE_CODE = """
import sqlite3

def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
"""

CLEAN_CODE = """
import sqlite3

def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()
"""

agent = build_security_agent(model_id="llama3.2:3b")

print("=== Vulnerable snippet (SQL injection) ===")
result1 = review(agent, VULNERABLE_CODE, "security")
print(result1.model_dump_json(indent=2))

print("\n=== Clean snippet ===")
result2 = review(agent, CLEAN_CODE, "security")
print(result2.model_dump_json(indent=2))