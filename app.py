from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

@app.route("/")
def home():
    data = list(db.mars_facts.find())
    
    return render_template("index.html", data=data)

@app.route('/scrape')
def scrape():
    db.collection.remove({})
    data = scrape_mars.scrape()
    db.collection.insert_one(data)
    return  render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

