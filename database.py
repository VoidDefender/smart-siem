import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from logger import get_logger

load_dotenv()

logger = get_logger("database")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            logger.info("Database connection established.")
            return connection

    except Error as e:
        logger.error(f"Database connection failed: {e}")
        raise

def execute_query(query, values=None, fetch=False):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        if fetch:
            return cursor.fetchall()

        connection.commit()
        logger.info("Query executed successfully.")

    except Error as e:
        logger.error(f"Query execution failed: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("Database connection closed.")

def insert_log(event):
    query = """
        INSERT INTO logs (event_type, username, ip_address, status)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        event["event_type"],
        event["username"],
        event["ip"],
        event["status"]
    )

    execute_query(query, values)

def insert_alert(alert_type, username, ip, message, severity):
    query = """
        INSERT INTO alerts (alert_type, username, ip_address, message, severity)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (alert_type, username, ip, message, severity)
    execute_query(query, values)
