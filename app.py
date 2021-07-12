from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
cluster = MongoClient(
    "mongodb+srv://anju:vilashni@workplease.s7aqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
count = collection.count_documents({})
print(count)


@app.route('/')
def index():
    return render_template('index.html', count=count)


@app.route("/users", methods=["POST"])
def create_user():
    return collection


if __name__ == '__main__':
    app.run(debug=True)
