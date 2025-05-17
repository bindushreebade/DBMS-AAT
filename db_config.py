import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['MYSQLHOST'],
        port=int(os.environ.get('MYSQLPORT', 3306)),
        user=os.environ['MYSQLUSER'],
        password=os.environ['MYSQLPASSWORD'],
        database=os.environ['MYSQLDATABASE']
    )
def test_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("✅ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Run the test
test_connection()