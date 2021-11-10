import os
from mysql.connector import MySQLConnection
import logging
from log import log

def connect_db():
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    log(0, "database connection", logging.INFO)
    return conn, cursor

def close_connect_db():
    conn.close()
    cursor.close()

def read_db_config():
    db = {
        "host": os.getenv("HOST"),
        "database": os.getenv("DATABASE"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD")
    }
    return db

# Переменные для подключения к БД
conn, cursor = connect_db()
