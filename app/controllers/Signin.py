"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Signin(Controller):
    def __init__(self, action):
        super(Signin, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('SigninModel')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('main.html')

    def create(self, method ='post'):
        # gather data posted to our create method and format it to pass it to the model
        user_info = {
             "name" : request.form['name'],
             "alias" : request.form['alias'],
             "email" : request.form['regemail'],
             "password" : request.form['regpassword'],
             "pw_confirmation" : request.form['regconfpassword'],
             "dob": request.form['dob']
        }
        # call create_user method from model and write some logic based on the returned value
        # notice how we passed the user_info to our model method
        create_status = self.models['SigninModel'].create_user(user_info)
        if create_status['status'] == True:
            # the user should have been created in the model
            # we can set the newly-created users id and name to session
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']
            #session['entrypoint']= 'registered'
            # we can redirect to the users profile page here
            return redirect('/quotes')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            # redirect to the method that renders the form
            return redirect('/main')
    def login(self, method='post'):
        user_info = {
             "email" : request.form['loginemail'],
             "password" : request.form['loginpassword'],
        }
        login_status = self.models['SigninModel'].login_user(user_info)
        if login_status['status'] == True:
            session['id']=login_status['user']['id']
            session['name']= login_status['user']['name']
            return redirect('/quotes')
        else:
            for message in login_status['errors']:
                flash(message, 'login_errors')
            # redirect to the method that renders the form
            return redirect('/main')
    def quotes(self):
        list_quotes = self.models['SigninModel'].get_all_quotes()
        list_favorite_quotes=self.models['SigninModel'].getfavoritequotes()
        return self.load_view('quotes.html', quote=list_quotes, favquote = list_favorite_quotes)

    def logoff(self):
        session.clear()
        return self.load_view('main.html')

    def addquotablequote(self, method='post'):
        # gather data posted to our create method and format it to pass it to the model
        quote_info = {
             "quoteauthor" : request.form['quoteauthor'],
             "content" : request.form['content'],
             "users_id" : session['id']
        }
        addquote_status = self.models['SigninModel'].add_quote(quote_info)
        if addquote_status['status'] == True:
            ##begin test code to insert into favs table##
            insert_into_favquotes = self.models['SigninModel'].add_into_favquotes()
            ##end test code to insert into favs table####
            return redirect('/quotes')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in addquote_status['errors']:
                flash(message, 'quote_errors')
            # redirect to the method that renders the form
            return redirect('/quotes')

    def addfavstatus(self, quoteid):
        favstatus_info = {
            "users_id": session['id'],
            "quote_id": quoteid
        }
        self.models['SigninModel'].add_favstatus(favstatus_info)
        return redirect('/quotes')

    def removefavstatus(self, quoteid):
        favstatus_remove_info = {
            "users_id": session['id'],
            "quote_id": quoteid
        }
        self.models['SigninModel'].remove_favstatus(favstatus_remove_info)
        return redirect('/quotes')

    def display(self, userid):
        display_info = {
            "users_id": userid,
        }
        posts = self.models['SigninModel'].getposts(display_info)
        return self.load_view('display.html', posts = posts)    


  


                    

