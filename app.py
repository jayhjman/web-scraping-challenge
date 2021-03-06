from flask import Flask, render_template, redirect, send_from_directory
from flask_pymongo import PyMongo
import scrape_mars
from pprint import pprint
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


#
# Clearing the collection out and forcing fetch of fresh data
#
mongo.db.mars_data.drop()


#
# Because your mongo collection could be empty
# on your initial fetch of "/" I made this generic
# function could be called in the future to scrape
# and poplate mongo before rendering the page.
#
# It is also used if an explicit scrape is requested.
#

def scrape_and_save_mars_data():

    # Set the collection name
    mars_data = mongo.db.mars_data

    # Call the scrape functions
    mars_info = scrape_mars.scrape()

    # print to the log to make sure we have data
    # pprint(mars_info)

    # Upsert the data, updating if needed, otherwise insert
    mars_data.update({}, mars_info, upsert=True)

    return mars_info


#
# Serve up the index.html template, if no data exists
# in MongoDB, then grab dummy mars_data and then display
#


@app.route("/")
def index():

    # Fetch the data from the database
    mars_data = mongo.db.mars_data.find_one()

    # Catches the first time through when there is no data
    if mars_data == None:
        # Below is for future use in case we want to
        # pre-load the mars_data
        #mars_data = scrape_and_save_mars_data()

        # give me back a dummy record for display
        mars_data = scrape_mars.build_dummy_mars_data()

    return render_template("index.html", mars_data=mars_data)

#
# Scrape the Mars pages and then redirect to the index page
# to display the latest Mars information
#


@app.route("/scrape")
def scraper():

    # I ignore the return values of this as I redirect
    # and it should be in the mongodb now
    scrape_and_save_mars_data()

    return redirect("/", code=302)

#
# Add favicon
#


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
