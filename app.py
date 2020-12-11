from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from pprint import pprint

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


def scrape_and_save_mars_data():

    # Set the collection name
    mars_data = mongo.db.mars_data

    # Call the scrape functions
    mars_info = scrape_mars.scrape()

    # print to the log to make sure we have data
    pprint(mars_info)

    # Upsert the data, updating if needed, otherwise insert
    mars_data.update({}, mars_info, upsert=True)

    return mars_info


# clear all existing data out of the collection.
# For demo purposes only,
# you may not want to do this for an app you're building!
mongo.db.mars_data.drop()


@app.route("/")
def index():

    # Fetch the data from the database
    mars_data = mongo.db.mars_data.find_one()

    # Catches the first time through when there is no data
    if mars_data == None:
        mars_data = scrape_and_save_mars_data()

    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():

    scrape_and_save_mars_data()

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
