import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import *
if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/upload_post', methods=['GET', 'POST'])
def upload_post():
    """ Finds user profile using the username in the database
    Checks to make sure the input is valid
    Adds a post to the database
    If not session redirects to login
    """
    # user_session = mongo.db.users.find_one({'username': session['user']})
    # user_pronouns = user_session['pronouns']
    # username = user_session['username']

    form = AddPostForm()

    if request.method == 'POST':
        post_date = datetime.now().strftime('%d/%m/%y, %H:%M')
        post_input = request.form.get('add_comment')
        post_type = request.form.get('post_type')

        post = {
            '_id': ObjectId(),
            'date': post_date,
            'author': username + " " + user_pronouns,
            'user_id': user_session['_id'],
            'post_input': post_input,
                'img_url': user_session['image_url'],
                'post_type': post_type,
                'comments': []
        }

        mongo.db.posts.insert_one(post)
        return redirect(url_for('review_stream'))

    return render_template('upload_post.html', form=form)


# Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    CREATE.
    Creates a new account for a new user; it calls the RegisterForm class
     from forms.py file.
    Checks if the username is not already excist in database,
    hashes the entered password and add a new user to session.
    '''
    # checks if user is not already has an account
    if 'username' in session:
        flash('You are already registered!')
        return redirect(url_for('homepage'))

    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        # checks if the username is unique
        registered_user = mongo.db.users.find_one({'username':
                                                   request.form['username']})
        if registered_user:
            flash("Sorry, this username is already taken!")
            return redirect(url_for('register'))
        else:
            # hashes the entered password using werkzeug
            hashed_password = generate_password_hash(request.form['password'])
            new_user = {
                "username": request.form['username'],
                "password": hashed_password,
                "email": request.form['email'],
                "personal_pronouns": request.form['personal_pronouns'],
                "occupation": request.form['occupation'],
                "tech_stack": request.form['tech_stack'],
                "about_me": request.form['about_me'],
            }
            users.insert_one(new_user)
            # add new user to the session
            session["username"] = request.form['username']
            flash('Your account has been successfully created.')
            return redirect(url_for('homepage'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
