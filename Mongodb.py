from bson import ObjectId
import pymongo
import json
from pymongo import MongoClient
def main():
    connection_to_database  = pymongo.MongoClient("mongodb://localhost:27017")
    CreateDatabase(connection_to_database)
    createCollections(connection_to_database)
    user_input_insertion(connection_to_database)
    categorie_search(connection_to_database)
    product_search_by_id(connection_to_database)
    delete = input("Do you want to delete and items from your cart enter 1 for yes and 0 for no:\n The program will end if you enter anyrthing else")
    delete = int(delete)
    if(delete == 1):
        cart_delete(connection_to_database)
    elif(delete == 0):
        order_summary(connection_to_database)
    else:
        print("Invalid input")
    userin=input("Do you want to view your order summary?If Yes enter 1 \n if not enter 0. \n if zero is entered program will end:")
    userin = int(userin)
    if(userin == 1):
        order_summary(connection_to_database)
    else:
        print("End of Program")
        return 0
def CreateDatabase(connection_to_database):
    databaselist=connection_to_database.list_database_names()
    if 'OnlineStore' not in databaselist:
        database = connection_to_database["OnlineStore"]
def createCollections(connection_to_database):
    database = connection_to_database["OnlineStore"]
    collections = database.list_collection_names()
    if 'Users' not in collections:
        database.create_collection("Users")
    if 'Products' not in collections:
        collection_two=database["Products"]
        load_data(collection_two)
    if 'ShoppingCart' not in collections:
        database.create_collection("ShoppingCart")
def load_data(collections):
    with open('/Users/admin/Documents/workspace/CS418/Project2mongoDB/Products.json') as file:
        file_data = json.load(file)
    e =0
    if(e == collections.count_documents({})):
        collections.insert_many(file_data)  
def user_input_insertion(database):
    first_name = input("Enter Your First name:") 
    last_name = input("Enter Your Last name:")
    Email_address = input("Enter Your Email Address:") 
    phone_number = input("Enter Your Phone Number:") 
    DOB = input("Enter your Date of Birth:") 
    collection = database["OnlineStore"]["Users"]
    collection.insert_one({"First_Name:":first_name,"Last_Name:":last_name,"Email_Address":Email_address,"Phone_Number:":phone_number,"DOB:":DOB})
def categorie_search(database):
    Categorie=input("Welcome to the online store \n Enter 1 to shop Mens clothing \n Enter 2 to shop Jewelry \n Enter 3 to shop Electronics \n Enter 4 to shop Women's Clothing")
    value =" "
    Categorie = int(Categorie)
    if(Categorie == 1):
        value = "men's clothing"
    if(Categorie ==2):
        value ="jewelery"
    if(Categorie == 3):
        value = "electronics"
    if(Categorie == 4 ):
        value = "women's clothing"
    else:
       print("Program ended beacuse you entered a invalid number")
    collection = database["OnlineStore"]["Products"]
    result = collection.find({"category":value})
    for d in result:
        print(d)
def product_search_by_id(database):
    id = int(input("\n \n \n \n Enter the product Id of the product you want to buy:"))
    collection = database["OnlineStore"]["Products"]
    result = collection.find({"$or": [{"id": id}, {"_id": id}]})
    add_to_shopping_cart(database,result)
def add_to_shopping_cart(database,products):
    databases = database["OnlineStore"]
    collections = databases["ShoppingCart"]
    for product in products:
        product.pop("_id", None)
        collections.insert_one(product)
def cart_delete(connection):
    itemid = int(input("Enter your Item ID you want to delete:"))
    database = connection["OnlineStore"]
    collection=database["ShoppingCart"]
    collection.delete_many({"id": itemid}) 
def order_summary(connection):
    database=connection["OnlineStore"]
    collection=database["ShoppingCart"]
    number= collection.count_documents({})
    number = str(number)
    print("There are:"+number+"of products in your cart.\n")
    result = collection.find()
    print("Here are the itmes in your cart")
    for doc in result:
        print(doc)
    result2 = collection.find({},{"price":1})
    main = float()
    for doc2 in result2:
        w= float(doc2["price"])
        main=main+w 
    final_total = "{:.2f}".format(main)
    final_total = float(final_total)
    final_total = round(final_total,2)
    print("Total cost is:"+ str(final_total))
if __name__ == "__main__":
    main()
