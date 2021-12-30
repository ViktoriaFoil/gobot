import BOT.bot as app

class Children_categories:

    def set_children_categories(self): #запрос на получение списка категорий
        name_query = "set_children_categories"
        query_to_db = "SELECT categories FROM `children_categories`;"
        return app.Database_query().simple_type_with_return(name_query, query_to_db)
