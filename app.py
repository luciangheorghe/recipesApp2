from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_pymongo import PyMongo
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MongoDB
app.config['MONGO_DBNAME'] = 'recipesapp89'
app.config['MONGO_URI'] = 'mongodb://lucas89:David2000@ds247439.mlab.com:47439/recipesapp89'


# init MongoDB
mongo = PyMongo(app)



# Home
@app.route('/')
def home():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Recipes
@app.route('/recipes')
def recipes():
    return render_template('recipes.html')


# Single Recipe
@app.route('/recipe/<string:id>/')
def recipe(id):
    return render_template('recipe.html', recipe=recipe)

#Register Form Class
class RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))



        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')



# Recipe Form Class
class RecipeForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    chef = StringField('Chef', [validators.Length(min=4, max=100)])
    level = StringField('Level', [validators.Length(min=4, max=100)])
    servings = IntegerField('Servings')
    reviews = IntegerField('Reviews')
    total = IntegerField('Total')

# Add Recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
@is_logged_in
def add_recipe():
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        chef = form.chef.data
        level = form.level.data
        servings = form.servings.data
        reviews = form.reviews.data
        total = form.total.data

        return redirect(url_for('dashboard'))

    return render_template('add_recipe.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
