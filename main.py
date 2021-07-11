import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://anju:vilashni@workplease.s7aqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]

# post = {"_id": 1, "name": "anju", "age": 19}

# post1 = {"_id": 16, "name": "sowmya", "age": 19}
# post2 = {"_id": 3, "name": "nithya", "age": 19}
# post3 = {"_id": 4, "name": "saiiii", "age": 19}
# post4 = {"_id": 5, "name": "yaswanthi", "age": 19}
# collection.insert(post1)
# collection.insert(post2)
# collection.insert_one(post3)
# collection.insert_one(post4)

# results = collection.find({})
# for i in results:
#     print(i)

# results = collection.delete_one({"_id": 16})

count = collection.count_documents({})
print(count)
