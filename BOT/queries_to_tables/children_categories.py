import queries_to_tables.database_query as query

def set_children_categories(): #запрос на получение списка категорий
    name_query = "set_children_categories"
    query_to_db = "SELECT categories FROM `children_categories`;"
    return query.simple_type_with_return(name_query, query_to_db)
