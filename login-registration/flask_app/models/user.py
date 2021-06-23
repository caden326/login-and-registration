from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_registration(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters..")
            is_valid = False
        if len(user['email']) < 8:
            flash("email must be valid")
            is_valid = False
        if len(user['password']) < 5:
            flash("password must be greater than 5 characters.")
            is_valid = False
        if (user['password']) != user['conf_password']:
            flash("passwords do not match.")
            is_valid = False
        return is_valid


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_registration").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s, NOW(), NOW() );"
        print("**********************")
        print(query)
        results = connectToMySQL("login_and_registration").query_db(query, data)
        return results

    @classmethod
    def user_info(cls,data):
        query= 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL("login_and_registration").query_db(query, data)
        return cls(results[0])