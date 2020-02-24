import pymongo
import os

password = os.getenv("MONGO_PWD")


client = pymongo.MongoClient(
    "mongodb+srv://disco_max:"
    + password
    + "@thecluster-ey2fy.mongodb.net/mars_app?retryWrites=true&w=majority"
)

try:
    print("MongoDB version is %s" % client.server_info()["version"])
    db = client.mars_app
    collection = db.mars_info
    print(collection)
    if collection:
        print("found mars_info")
    else:
        print("not found")

except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)

