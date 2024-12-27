import mysql.connector

def get_connection():
    """Returns a MySQL database connection."""
    connection = mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="23uZZvie28b3HCB.root",
        password="K0QwN6VXC8TdWpsu",
        database="sarvam",
        ssl_ca="/etc/ssl/cert.pem",
    )
    return connection

def execute_query(query, params=None):
    """
    Executes a SQL query and returns the result.
    For SELECT queries: returns fetched data
    For INSERT/UPDATE/DELETE queries: returns affected rows or last insert id
    """
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        # Check if the query is a SELECT query
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            # For INSERT/UPDATE/DELETE queries
            connection.commit()
            if cursor.lastrowid:
                result = cursor.lastrowid
            else:
                result = cursor.rowcount
                
        return result
    
    except mysql.connector.Error as err:
        if connection:
            connection.rollback()
        print(f"Database error: {err}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()