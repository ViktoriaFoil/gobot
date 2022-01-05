from queries_to_tables.db_query import Database_query


class Children_categories:

    @staticmethod
    def set_children_categories():
        name_query = "set_children_categories"
        query_to_db = "SELECT categories FROM `children_categories`;"
        return Database_query.simple_type_with_return(name_query, query_to_db)
