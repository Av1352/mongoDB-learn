
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://sakura:sakura@user.g2qy7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["user"]
collection_signup = db["posts"]
print("db connected")
# print(db)
# print(collection_signup)

# post = {"username": "yash", "tweet": "Hey . looking for partners in a medical project. #partnership #medical #business #entrepreneur" }
# b = {"username": "sowmya", "tweet": "looking to investing in a financial project #investment #finance #business #entrepreneur" }
# c= {"username": "elon musk", "tweet": "willing to get employed in a technical project #employee #hire #tech #business #entrepreneur" }

my_string = "invest partner"  # THIS IS WHERE WE INSERT GET FROM FORM !!!!!!!!!!

# collection_signup.insert_one(post)
# collection_signup.insert_one(b)
# collection_signup.insert_one(c)

def convert(my_search):
    return (my_search[0].split())


my_search = [my_string]
# print(my_search)
converted_to_list_search = convert(my_search)  #search values converted to a list of words
# print(converted_to_list_search)

query =db.posts.find( { "$text": { "$search": my_string } } ).sort("_id", -1)

# query = cursor_loc.find_one( { "$text": { "$search": "invest collaborate project" } } )
""
# print(collection_signup.list_indexes())
# print(query)
# print(list(query))
# a = db.posts.create_index([('$**', 'text')])
# print(a)
final_search_results=[]

for i in query:
    if i not in final_search_results:
        final_search_results.append(i)
        # print("appended")
    # print(i)

for word in converted_to_list_search:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.append(lm.name())
    # adding into synonyms
    final_list_of_synonyms = (list(set(synonyms)))
    # print(final_list_of_synonyms)
# print("-----------------------------------------------------------------")
for each_word in final_list_of_synonyms:
        query_for_synonym_words_search_result = db.posts.find({"$text": {"$search": each_word}}).sort("_id", -1)
        for k in query_for_synonym_words_search_result:
            if k not in final_search_results:
                final_search_results.append(k)
                # print("appended")
            # print(k)

# print("-----------------------------------------------------------------")
for result in final_search_results:
    print(result)