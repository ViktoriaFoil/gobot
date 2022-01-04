import logging

from APP.config.mysql import Mysql
from APP.logs.log import log


class Database_query:

    @staticmethod
    def simple_type_without_return(name_query, query):
        try:
            Mysql.cursor.execute(query)
            Mysql.conn.commit()
        except BaseException as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_return(name_query, query):
        try:
            Mysql.cursor.execute(query)
            result = Mysql.cursor.fetchall()
            Mysql.conn.commit()
            return result
        except BaseException as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_cycle(name_query, array, query):
        try:
            Mysql.cursor.execute(query)
            result = Mysql.cursor.fetchall()
            for item in result:
                array.append(item[0])
            Mysql.conn.commit()
            return array
        except BaseException as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_condition(name_query, query):
        try:
            line = ''
            Mysql.cursor.execute(query)
            result = Mysql.cursor.fetchall()
            if any(result):
                line = result[0][0]
            return str(line)
        except BaseException as e:
            log(0, f"error {name_query} {e}", logging.ERROR)
