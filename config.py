import os

password = os.getenv("MONGO_PWD")

uri_string = (
    "mongodb+srv://disco_max:"
    + password
    + "@thecluster-ey2fy.mongodb.net/test?retryWrites=true&w=majority"
)

