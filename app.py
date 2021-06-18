import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date
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


@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)    


@app.route('/review_stream')
def review_stream(username):
    return render_template('review_stream.html')    


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
        post_input = request.form['post_input']
        post_type = request.form['post_type']
        print(post_input)
        print(post_type)

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


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
