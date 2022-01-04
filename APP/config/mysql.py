import logging
import os
import mariadb
from APP.logs.log import log

class Mysql:

    @staticmethod
    def connect_db():
        conn = mariadb.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"))

        cursor = conn.cursor()
        log(0, "database connection", logging.INFO)
        return conn, cursor

    @staticmethod
    def close_connect_db():
        Mysql().conn.close()
        Mysql().cursor.close()


    conn, cursor = connect_db()
