from os import stat
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
from flask import flash

class Recipe:
    db_name = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.under_30 = data["under_30"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        result = MySQLConnection(cls.db_name).query_db(query)
        all_recipes = []
        for row in result:
            this_recipe = cls(row)
            all_recipes.append(this_recipe)
        return all_recipes


    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes(name, description, under_30, instructions, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(under_30)s, %(instructions)s, NOW(), NOW(), %(user_id)s);"
        return MySQLConnection(cls.db_name).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name =%(name)s, description = %(description)s, under_30 = %(under_30)s, instructions = %(instructions)s, updated_at = NOW(), user_id = %(user_id)s WHERE id = %(id)s; "
        return MySQLConnection(cls.db_name).query_db(query, data)

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return MySQLConnection(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data["name"]) < 3:
            flash("name should be larger than 3 characters", "recipe")
            is_valid = False
        if len(data["description"]) < 3:
            flash("description should be larger than 3 characters", "recipe")
            is_valid = False
        if len(data["instructions"]) < 3:
            flash("instructions should be larger than 3 characters", "recipe")
            is_valid = False
        return is_valid

