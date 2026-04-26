import mysql.connector

def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kiruthika@1991",
            database="drink_db"
        )
        return conn

    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None