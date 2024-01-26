
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask_app.models import user
# import re
# from flask_bcrypt import Bcryp
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Post:
    db = "dojo_wall" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?
        self.creator = None


    # Create Users Models
    @classmethod
    def create_new_post(cls, post_data):
        if not cls.validate_post(post_data): return False
        query = """
            INSERT INTO posts (content, user_id)
            VALUES (%(content)s, %(user_id)s);"""
        results = connectToMySQL(cls.db).query_db(query,post_data)
        return results


    # Read Users Models
    @classmethod
    def get_post_by_id(cls,id):
        data = {'id': id}
        query = """
            SELECT *
            FROM users
            WHERE id = %(data)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    
    @classmethod
    def get_all_posts_with_creator(cls):
        query = """
            SELECT *  
            FROM posts
            LEFT JOIN users 
            ON users.id = posts.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        for result in results:
            this_post = cls(result)
            this_post.creator = user.User.instantiate_user(result)
            all_posts.append(this_post)
        return all_posts


    # Delete Post Models
    @classmethod
    def delete_user_post(cls,data):
        post_id = {'id' : data}
        query = """
            DELETE FROM posts
            where id = %(id)s;"""
        connectToMySQL(cls.db).query_db(query, post_id)
        return 

    # validations
    
    @classmethod
    def validate_post(cls, data):
        is_valid = True
        if len(data['content']) < 1:
            flash("You cannot publish a blank post.")
            is_valid = False
        return is_valid
