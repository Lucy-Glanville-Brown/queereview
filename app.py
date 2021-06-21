import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date, datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from forms import *
from utilities import *
if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

mongo = PyMongo(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    """ Profile page
    Finds the profile from the username returns - user_profile
    """

    if 'username' in session:
        user_session = mongo.db.users.find_one(
            {'username': session['username']})['_id']
        user_profile = mongo.db.users.find_one(
            {'username': username})

        if not user_profile:
            flash('Woops profile not found')
            return render_template('profile_not_found.html')

        user_id = mongo.db.users.find_one(
            {'username': session['username']})['_id']
        my_posts = mongo.db.posts.find({'user_id': user_id})
        my_comments = mongo.db.posts.find(
            {'comments.comment_user_id': ObjectId(user_id)})

        return render_template(
            'profile.html',
            username=username,
            user_profile=user_profile,
            user_session=user_session,
            my_posts=my_posts, my_comments=my_comments
        )

    else:
        flash("Please log in to view this page")
        return redirect(url_for('login'))

    return render_template('profile.html', username=username)


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    """ Edit Profile page
    Finds the profile from the username and allow user to update profile details
    """

    user_profile = mongo.db.users.find_one({"username": session['username']})
    form = UpdateProfileForm()

    if form.validate_on_submit():
        print('valid')
        users = mongo.db.users
        users.update_one({"username": username},
                         {'$set': {
                             "email": request.form['email'],
                             "personal_pronouns": request.form['personal_pronouns'],
                             "occupation": request.form['occupation'],
                             "tech_stack": request.form['tech_stack'],
                             "about_me": request.form['about_me'],
                         }})

        flash('Your details have been successfully update.')
        return redirect(url_for('profile', username=username))

    return render_template('edit_profile.html', username=session['username'], user_profile=user_profile, form=form)


@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """ Edit Profile page
    Finds the profile from the username and allow user to update profile details
    """

    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    formCode = AddCodeForm()
    formReview = AddReviewForm()
    formGeneral = AddGeneralForm()

    if formCode.validate_on_submit() or formReview.validate_on_submit() or formGeneral.validate_on_submit():

        post_update = update_post()

        mongo.db.posts.update_one({"_id": ObjectId(post_id)},
                                  {'$set':
                                   post_update
                                   })

        flash('Your post has been successfully update.')
        return redirect(url_for('post', post_id=post_id))

    return render_template('edit_post.html', post=post, formCode=formCode,
                           formReview=formReview,
                           formGeneral=formGeneral)


@app.route('/review_stream')
def review_stream():
    posts = mongo.db.posts.find()
    return render_template('review_stream.html', posts=posts)


@app.route('/users')
def users():
    users = mongo.db.users.find()
    return render_template('users.html', users=users)


@app.route('/allyandsupport')
def ally():
    return render_template('ally.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username')})

        if existing_user:
            if check_password_hash(
                    existing_user['password'],
                    request.form.get('password')):
                session['username'] = request.form.get('username')
                return redirect(url_for('review_stream'))
        else:
            flash("Either your username or password was incorrect")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/upload_post', methods=['GET', 'POST'])
def upload_post():
    """ Finds user profile using the username in the database
    Checks to make sure the input is valid
    Adds a post to the database
    If not session redirects to login
    """

    formCode = AddCodeForm()
    formReview = AddReviewForm()
    formGeneral = AddGeneralForm()

    if 'username' not in session:
        flash("Please log in to make a post")
        return redirect(url_for('login'))

    user_session = mongo.db.users.find_one({'username': session['username']})
    user_pronouns = user_session['personal_pronouns']
    username = user_session['username']
    user_id = user_session['_id']

    if formCode.validate_on_submit() or formReview.validate_on_submit() or formGeneral.validate_on_submit():

        post = get_post(user_pronouns, username, user_id)

        mongo.db.posts.insert_one(post)

        return redirect(url_for('review_stream'))
    return render_template('upload_post.html', formCode=formCode,
                           formReview=formReview,
                           formGeneral=formGeneral)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    """ Post page
    Finds the post from the username returns - user_profile
    """

    form = AddCommentForm()

    if 'username' in session:
        post = mongo.db.posts.find_one(
            {'_id': ObjectId(post_id)})

        session_user = mongo.db.users.find_one(
            {'username': session['username']})['_id']

        if not post:
            flash('Woops post not found')
            return render_template('profile_not_found.html')

        if form.validate_on_submit():
            comment_date = datetime.now().strftime('%d/%m/%y, %H:%M')
            comment_input = request.form['comment_input']
            comment_id = ObjectId()
            session_user = mongo.db.users.find_one(
                {'username': session['username']})

            mongo.db.posts.update_one(
                {'_id': ObjectId(post_id)},
                {'$addToSet': {'comments': {
                    'comment_id': comment_id,
                    'date': comment_date,
                    'author': session_user['username'] + " " + session_user['personal_pronouns'],
                    'comment_user_id': session_user['_id'],
                    'username': session_user['username'],
                    'post_id': ObjectId(post_id),
                    'comment_input': comment_input,
                    'post_title_comment': post['post_title']
                }}})

            return render_template(
                'post.html',
                post=post, form=form, post_id=post_id
            )

    else:
        flash("Please log in to view this page")
        return redirect(url_for('login'))

    return render_template('post.html', post=post, form=form, session_user=session_user)


@app.route("/<username>/upload_image", methods=["GET", "POST"])
def upload_image(username):

    if request.method == 'POST':
        for item in request.files.getlist("user_image"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_image = (username + '/q_auto:low/' + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image)
            image_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/c_fit,h_250,w_250/doubleshamrocks/"
                + public_id_image + file_extension)

            mongo.db.users.update(
                {"username": session['username']},
                {"$set": {"profile_image": image_url}})

        return redirect(url_for('profile', username=session['username']))
    return render_template("profile.html", username=session['username'])


@app.route("/<username>/upload_cover", methods=["GET", "POST"])
def upload_cover(username):

    if request.method == 'POST':
        for item in request.files.getlist("cover_image"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_image = (username + '/q_auto:low/' + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image)
            image_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/doubleshamrocks/"
                + public_id_image + file_extension)

            mongo.db.users.update(
                {"username": session['username']},
                {"$set": {"cover_image": image_url}})

        return redirect(url_for('profile', username=session['username']))
    return render_template("profile.html", username=session['username'])
# Register


@ app.route("/register", methods=['GET', 'POST'])
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


@ app.route('/delete_profile/<username>', methods=['GET', 'POST'])
def delete_profile(username):
    if session['username'] == username:
        mongo.db.users.remove({'username': session['username']})
        flash("Your profile has been succesfully deleted")
    return redirect(url_for('/'))


@ app.route('/delete_comment/<post>/<comment_id>', methods=['GET', 'POST'])
def delete_comment(post, comment_id):
    mongo.db.posts.update_one(
        {'_id': ObjectId(post)},
        {'$pull': {'comments': {'comment_id': ObjectId(comment_id)}}})
    flash("Your profile has been succesfully deleted")
    return redirect(url_for('post', post_id=post))


@ app.route('/delete_post/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):

    mongo.db.posts.remove({'_id': ObjectId(post_id)})
    flash("Your post has been succesfully deleted")
    return redirect(url_for('profile', username=session['username']))


@ app.route('/logout')
def logout():
    """ Removes session cookie and tells user they are logged out
    """
    session.pop('username')
    flash("You have been logged out")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
