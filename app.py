from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars
from config import uri_string


app = Flask(__name__)
app.config["MONGO_URI"] = uri_string
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# driver with connection string for use with MongoDB Atlas AWS cloud service:
# client = pymongo.MongoClient("mongodb+srv://disco_max:<password>@cluster0-ey2fy.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    if mars_info is None:
        mars_info = {
            "news_title": "Press Button",
            "news_paragraph": "Press Button",
            "featured_image": "Press Button",
            "mars_weather": "Press Button",
            "mars_facts": "Press Button",
            "hemisphere_image_urls": [
                "Press Button",
                "Press Button",
                "Press Button",
                "Press Button",
            ],
        }
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    data = scrape_mars.scrape_info()
    mars_info.replace_one({}, data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
