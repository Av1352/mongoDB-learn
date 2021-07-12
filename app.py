import os

from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
app_root = os.path.abspath(os.path.dirname(__file__))

cluster = MongoClient(
    "mongodb+srv://anju:vilashni@workplease.s7aqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
count = collection.count_documents({})


@app.route('/')
def index():
    return render_template('index.html', count=count)


@app.route("/users", methods=["GET", "POST"])
def create_users():
    if request.method == "POST":
        # id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        print(name, age)
        keys = ["name", "age"]
        values = []
        values.extend((name, age))
        dict1 = to_dictionary(keys, values)
        print(dict1)
        collection.insert_one(dict1)
        return render_template("users.html")
    if request.method == "GET":
        return render_template("users.html")


def to_dictionary(keys, values):
    return dict(zip(keys, values))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method =="POST":
        email = request.form.get('email')
        password = request.form.get('pass')
        return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)
