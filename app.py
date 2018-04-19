from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MongoDB
app.config['MONGO_DBNAME'] = 'recipesapp89'
app.config['MONGO_URI'] = 'mongodb://lucas89:David2000@ds247439.mlab.com:47439/recipesapp89'


# Init MongoDB
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
    recipes = mongo.db.recipes

    find_recipes = mongo.db.recipes.find()

    if find_recipes > 0:
        return render_template('recipes.html', recipes=find_recipes)
    else:
        msg = 'No Recipes Found'
        return render_template('recipes.html', msg=msg)
    # return render_template('recipes.html')


# Single Recipe
@app.route('/recipes/<recipe_id>')
def recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    return render_template('recipe.html', recipe=the_recipe)

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
        password = sha256_crypt.encrypt(str(form.password.data))

        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            users.insert({'first_name': request.form['first_name'], 'last_name': request.form['last_name'], 'email': request.form['email'], 'username': request.form['username'], 'password': password})
            session['username'] = request.form['username']
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))

        flash('That username already exists!', 'danger')

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user > 0:
            password = sha256_crypt.encrypt(str(form.password.data))

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

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

    recipes = mongo.db.recipes

    find_recipes = mongo.db.recipes.find()

    if find_recipes > 0:
        return render_template('dashboard.html', recipes=find_recipes)
    else:
        msg = 'No Recipes Found'
        return render_template('dashboard.html', msg=msg)

# Recipe Form Class
class RecipeForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    chef = StringField('Chef', [validators.Length(min=4, max=100)])
    reviews = IntegerField('Reviews')

    total = IntegerField('Total')
    prep = IntegerField('Prep')
    cook = IntegerField('Cook')
    inactive = IntegerField('Inactive')

    level = StringField('Level', [validators.Length(min=4, max=100)])
    servings = IntegerField('Servings')

    calories = IntegerField('Calories')
    total_fat = IntegerField('Total Fat')
    saturated_fat = IntegerField('Saturated Fat')
    cholesterol = IntegerField('Cholesterol')
    sodium = IntegerField('Sodium')
    carbohydrats = IntegerField('Carbohydrats')
    diestary_fiber = IntegerField('Diestary Fiber')
    protein = IntegerField('Protein')
    sugar = IntegerField('Sugar')

    ingredients = StringField('Ingredients', [validators.Length(min=4, max=1000)])

    directions = StringField('Directions', [validators.Length(min=4, max=1000)])

    categories = StringField('Categories', [validators.Length(min=4, max=1000)])

# Add Recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
@is_logged_in
def add_recipe():
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():

        recipes = mongo.db.recipes
        existing_recipe = recipes.find_one({'title': request.form['title']})

        if existing_recipe is None:
            recipes.insert({'title': request.form['title'],
            'reviews': request.form['reviews'],
            'chef': request.form['chef'],

            'time': {'total': request.form['total'],
            'prep': request.form['prep'],
            'cook': request.form['cook'],
            'inactive': request.form['inactive']},

            'servings': request.form['servings'],
            'level': request.form['level'],
            'nutrition': {'calories': request.form['calories'],
            'total_fat': request.form['total_fat'],
            'saturated_fat': request.form['saturated_fat'],
            'cholesterol': request.form['cholesterol'],
            'sodium': request.form['sodium'],
            'carbohydrats': request.form['carbohydrats'],
            'diestary_fiber': request.form['diestary_fiber'],
            'protein': request.form['protein'],
            'sugar': request.form['sugar']},


            'ingredients': request.form['ingredients'],
            'directions': request.form['directions'],
            'categories': request.form['categories'],})

        flash('Recipe Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_recipe.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
