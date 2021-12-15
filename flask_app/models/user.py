from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return MySQLConnection(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        if len(result) == 0:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        return cls(result[0])



    @staticmethod
    def validate_registration(data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = MySQLConnection("recipes_schema").query_db(query, data)
        is_valid = True
        if len(result) != 0:
            flash("email already exists", "register")
            is_valid = False
        if len(data["first_name"]) <= 1:
            flash("First Name should be longer than 1 character", "register")
            is_valid = False
        if len(data["last_name"]) <= 1:
            flash("Last Name should be longer than 1 character", "register")
            is_valid = False
        if len(data["email"]) == 0:
            flash("Enter an Email", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Enter a valid Email", "register")
            is_valid = False
        if len(data["password"]) == 0:
            flash("Enter a Password", "register")
            is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash("passwords do not match", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if len(data["email"]) == 0:
            flash("Enter an email", "login")
            is_valid = False
        if len(data["password"]) == 0:
            flash("Enter a password", "login")
            is_valid = False
        return is_valid

    @staticmethod
    def can_delete(user_id, recipes):
        delete_list = {
        }
        for recipe in recipes:
            if recipe.user_id == user_id.id:
                delete_list[recipe.id] = "delete"
            else:
                delete_list[recipe.id] = ""
        return delete_list
    
    @staticmethod
    def can_edit(user_id, recipes):
        delete_list = {
        }
        for recipe in recipes:
            if recipe.user_id == user_id.id:
                delete_list[recipe.id] = "edit"
            else:
                delete_list[recipe.id] = ""
        return delete_list
