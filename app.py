from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# driver with connection string for use with MongoDB Atlas AWS cloud service:
# client = pymongo.MongoClient("mongodb+srv://disco_max:<password>@cluster0-ey2fy.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    data = scrape_mars.scrape_info()
    mars_info.replace_one({}, data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
