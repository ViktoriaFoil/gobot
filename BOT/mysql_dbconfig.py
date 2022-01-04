import os
import mariadb
import logging
from log import log


def connect_db():
    conn = mariadb.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"))

    cursor = conn.cursor()
    log(0, "database connection", logging.INFO)
    return conn, cursor


def close_connect_db():
    conn.close()
    cursor.close()


conn, cursor = connect_db()
