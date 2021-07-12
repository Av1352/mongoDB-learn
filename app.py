import os

import bcrypt
from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "super secret key"
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
        # keys_signup = ["name", "email", "password"]
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        re_pass = request.form.get('re_pass')
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
            # inserting them in a dictionary in key value pairs
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
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('your_pass')

        # check if email exists in database
        email_found = collection_signup.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
