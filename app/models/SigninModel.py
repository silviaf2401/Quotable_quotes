""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re 

class SigninModel(Model):
    def __init__(self):
        super(SigninModel, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """
    def create_user(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        # Some basic validation
        if not info['name']:
            errors.append('Name cannot be blank')
        if not info['alias']:
            errors.append('Alias cannot be blank')    
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        if not info['dob']:
            errors.append('Date of birth cannot be blank')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
        # bcrypt is now an attribute of our model
        # we will call the bcrypt functions similarly to how we did before
        # here we use generate_password_hash() to generate an encrypted password
            email = info['email']
            user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            query_data = { 'email': email }
            user = self.db.query_db(user_query, query_data)
            if user != []:
                errors.append("An account is already associated with that e-mail address, please login instead")
                return {"status": False, "errors": errors}
            else:
                hashed_pw = self.bcrypt.generate_password_hash(password)
                create_query = "INSERT INTO users (name, alias, email, pw_hash, dob, created_at) VALUES (:name, :alias, :email, :pw_hash, :dob, NOW())"
                create_data = {'name': info['name'], 'alias': info['alias'], 'email': info['email'], 'pw_hash': hashed_pw, 'dob': info['dob']}
                self.db.query_db(create_query, create_data)# Code to insert user goes here...
            # Then retrieve the last inserted user.
                get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
                users = self.db.query_db(get_user_query)
                return { "status": True, "user": users[0] } 
    def login_user(self, user_info): 
        errors=[]
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': user_info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], user_info['password']):
                return {"status": True, "user": user[0]}
        errors.append('User was not found in database. Please try a different user name/password combination or register instead')
        # Whether we did not find the email, or if the password did not match, either way return False
        return {"status": False, "errors": errors}  

    def add_quote(self, quote_info):
        errors = []
        # Some basic validation
        if not quote_info['quoteauthor']:
            errors.append('Author cannot be blank')
        elif len(quote_info['quoteauthor']) < 4:
            errors.append('Author must be at least 4 characters long')
        if not quote_info['content']:
            errors.append('Message cannot be blank')
        elif len(quote_info['content']) < 11:
            errors.append('Author must be at least 11 characters long')
        if errors:
            return {"status": False, "errors": errors}
        else:
            quoteauthor = quote_info['quoteauthor']
            content = quote_info['content']
            users_id = quote_info['users_id']
            add_query = "INSERT INTO quotablequotes (quoteauthor, content, whoadded, created_at) VALUES (:quoteauthor, :content, :whoadded, NOW())"
            add_data = {'quoteauthor': quote_info['quoteauthor'], 'content': quote_info['content'], 'whoadded': quote_info['users_id']}
            self.db.query_db(add_query, add_data)# Code to insert user goes here...
            # Then retrieve the last inserted user.
            #get_quote_query = "SELECT * FROM quotablequotes ORDER BY id DESC LIMIT 1" 
            #quotablequotes = self.db.query_db(get_quote_query)
            return { "status": True }    

    def get_all_quotes(self):
        #list_quotes = self.db.query_db("SELECT quoteauthor, content, whoadded FROM quotablequotes ORDER BY created_at DESC")
        #list_authors = self.db.query_db("SELECT * FROM users ORDER BY id DESC")
        #return list_quotes, list_authors
        #list_quotes = self.db.query_db("SELECT users.name, quoteauthor, content, quotablequotes.id from quotablequotes join users on users.id = quotablequotes.whoadded ORDER BY quotablequotes.created_at DESC")
        list_quotes = self.db.query_db("SELECT users.name, quoteauthor, content, quotablequotes.id, whoadded from quotablequotes join users on users.id = quotablequotes.whoadded join users_quotes_favs on users_quotes_favs.quotablequotes_id = quotablequotes.id WHERE users_quotes_favs.favorite_status = 0 ORDER BY quotablequotes.created_at DESC")
        return list_quotes

    def add_into_favquotes(self):
        get_quote_query = "SELECT * FROM quotablequotes ORDER BY id DESC LIMIT 1" 
        quotablequotes = self.db.query_db(get_quote_query)
        print "this is it!", quotablequotes
        insert_query = "INSERT INTO users_quotes_favs(quotablequotes_id, users_id, favorite_status) VALUES (:quotablequotes_id, :users_id, :favorite_status)"
        insert_data = {'quotablequotes_id': quotablequotes[0]['id'] , 'users_id': quotablequotes[0]['whoadded'], 'favorite_status': 0}
        self.db.query_db(insert_query, insert_data)

    def add_favstatus(self, favstatus_info):
        add_favstatus_query = "UPDATE users_quotes_favs SET favorite_status =1 WHERE (users_id = :users_id) AND (quotablequotes_id = :quotablequotes_id)"
        add_favstatus_data = {'users_id': favstatus_info['users_id'], 'quotablequotes_id': favstatus_info['quote_id']} 
        self.db.query_db(add_favstatus_query, add_favstatus_data)

    def getfavoritequotes(self):
        list_favorite_quotes = self.db.query_db("SELECT users.name, quoteauthor, content, quotablequotes.id from quotablequotes join users on users.id = quotablequotes.whoadded join users_quotes_favs on users_quotes_favs.quotablequotes_id = quotablequotes.id WHERE users_quotes_favs.favorite_status = 1 ORDER BY quotablequotes.created_at DESC")
        return list_favorite_quotes

    def remove_favstatus(self, favstatus_remove_info):
        remove_favstatus_query = "UPDATE users_quotes_favs SET favorite_status =0 WHERE (users_id = :users_id) AND (quotablequotes_id = :quotablequotes_id)"
        remove_favstatus_data = {'users_id': favstatus_remove_info['users_id'], 'quotablequotes_id': favstatus_remove_info['quote_id']} 
        self.db.query_db(remove_favstatus_query, remove_favstatus_data)

    def getposts(self, display_info):
        print "this is display_info", display_info
        posts_query = "SELECT quoteauthor, content, users.name FROM quotablequotes join users on users.id = quotablequotes.whoadded WHERE whoadded =:whoadded ORDER BY quotablequotes.created_at DESC"
        posts_data = {'whoadded': display_info['users_id']}
        posts = self.db.query_db(posts_query, posts_data)
        posts[0]['num_quotes'] = len(posts)
        return posts    
                 