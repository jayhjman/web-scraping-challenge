from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from pprint import pprint

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

# clear all existing data out of the collection.
# For demo purposes only,
# you may not want to do this for an app you're building!
mongo.db.mars_data.drop()


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()

    pprint(mars_info)

    mars_data.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
