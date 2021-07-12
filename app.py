import os

import bcrypt
from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app_root = os.path.abspath(os.path.dirname(__file__))

# <-------- MONGO CONNECTION -------->

cluster = MongoClient(
    "mongodb+srv://anju:vilashni@workplease.s7aqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
collection_signup = db["signup"]
count_test = collection.count_documents({})
count_signup = collection_signup.count_documents({})


def to_dictionary(keys, values):
    return dict(zip(keys, values))


# <-------- APP ROUTES -------->


@app.route('/')
def index():
    return render_template('index.html', count_test=count_test, count_signup=count_signup)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        keys_signup = ["name", "email", "password"]
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        re_pass = request.form.get('re_pass')
        # values = []
        # values.extend((name, email, password))
        # dict_signup = to_dictionary(keys_signup, values)
        # print(dict_signup)
        # collection_signup.insert_one(dict_signup)
        # if found in database showcase that it's found
        user_found = collection_signup.find_one({"name": name})
        email_found = collection_signup.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('signup.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)
        if password != re_pass:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(re_pass.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': name, 'email': email, 'password': hashed}
            # insert it in the record collection
            collection_signup.insert_one(user_input)

            # find the new created account and its email
            user_data = collection_signup.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)

    if request.method == "GET":
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('your_name')
        password = request.form.get('your_pass')
        print(username, password)
        return render_template("login.html")
    if request.method == "GET":
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
