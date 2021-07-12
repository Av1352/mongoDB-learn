from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://anju:vilashni@workplease.s7aqg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
collection1 = db["signup"]


#
# post = {"_id": 1, "name": "anju", "age": 19}
#
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
#
# results = collection.delete_one({"_id": 16})
#
# count = collection.count_documents({})
# print(count)

# collection.insert_one({"name": "john", "age": 76})
def to_dictionary(keys, values):
    return dict(zip(keys, values))

keys = ["name", "email", "password"]
name = input("Enter name: ")
email = input("Enter email: ")
password = input("Enter password: ")
values = []
values.extend((name, email, password))
dict1 = to_dictionary(keys, values)
print(dict1)
collection1.insert_one(dict1)
