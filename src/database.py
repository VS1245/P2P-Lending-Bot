from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
uri = "mongodb+srv://shambhaviverma:197376200005@desis.a9ikza8.mongodb.net/?retryWrites=true&w=majority&appName=DESIS"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["P2PLend"]
try:
    client.admin.command('ping')
except Exception as e:
    print(e)

def authenticate():
     #check if the details are authentic or not
     return True

def group_creation(name, admin_id, admin_password, join_code):
    
    record = {"name": name, "admin_id": admin_id, "admin_password": admin_password, "join_code": join_code}
    collection = db["Groups"]

    if(collection.find_one({"name":name})):
        return "Group Name Not Available"
    
    collection.insert_one(record)
    return "Group Created"

def add_member(group_name, join_code, member_id, authentication_details):

    group = db["Groups"]
    document = group.find_one({"name": group_name})
    if not (document):
        return "No such group exists"
       
    if not (group.find_one({"name": group_name, "join_code": join_code})):
        return "Group Join Code Incorrect"
    
    group_id = document.get("Group_id")
    if not authenticate():
         return "Member details are not authentic"
    
    record = {"Member_name": member_id, "Group_id": group_id, "authentication details": authentication_details, "points" : 0}
    member_collections = db["Members"]
    member_collections.insert_one(record)

def add_transaction(borrower_id, lender_id, group_id, amount, time):
    transaction = db["Transaction"]
    record = {"Borrower_id": borrower_id, "Lender_id": lender_id, "Group_id": group_id, "Amount": amount, "Time" : time, "Return_status": "Pending"}
    transaction.insert_one(record)

def admin_login(admin_id, admin_password, group_name):
    group = db["Groups"]
    if not (group.find_one({"admin_id": admin_id, "admin_password": admin_password, "name": group_name})):
        return "Incorrect Credentials"
    
def remove_member(member_name, group_name):
    collection = db["Members"]
    group_id = db["Groups"].find_one({"name": group_name}).get("_id")
    print(group_id)
    result = collection.delete_one({"Member_name": member_name, "Group_id": group_id})
    if result.deleted_count == 1:
        return "Member removed successfully."
    else:
        return "Entry not found." 

def get_admin_id(group_name):
    group = db["Groups"]
    document = group.find_one({"name": group_name})
    if document:
        return document.get("admin_id")
    return None

def is_join_code_correct(group_name, join_code):
    group = db["Groups"]
    document = group.find_one({"name": group_name, "join_code": join_code})
    return bool(document)

def is_group_exists(group_name):
    group = db["Groups"]
    document = group.find_one({"name": group_name})
    return bool(document)
