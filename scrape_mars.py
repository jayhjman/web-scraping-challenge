# Import scraping libraries and anything else needed
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint
import pandas as pd

#
# Initializing the splinter browser plug in
#


def init_browser():
    # @NOTE: My chromedriver is on the system PATH for this to work
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#
# Go to https://mars.nasa.gov/news/ and scrape the latest mars news
#


def scrape_mars_news():

    browser = init_browser()

    # Visit https://mars.nasa.gov/news/
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #  Delay so we can finish reading the page
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Grab the list of news articles
    news_snippet = soup.find("ul", class_="item_list")

    # print(news_snippet.prettify())

    # The articles are contained in a list of slides
    slide_list = soup.find_all("li", class_="slide")

    # grab the first slide as it is the latest article
    news_p = slide_list[0].find(
        "div", class_="rollover_description_inner").get_text()
    news_title = slide_list[0].find("h3").get_text()

    # Quit the browser after scraping
    browser.quit()

    # Return results
    return {
        "news_title": news_title,
        "news_p": news_p,
    }

#
# Go to https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars and scrape the featured image
#
# This does change time to time so don't be surprised if it changes between calls
#


def scrape_mars_featured_image():

    browser = init_browser()

    # Visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Delay so we can finish reading the page
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the full_image link to further traverse down
    image_snippet = soup.find("a", id="full_image")

    # data-link has a landing page that can be used to get the full image link
    image_link = image_snippet["data-link"]
    image_link = url.split("/spaceimages")[0] + image_link

    # print(image_snippet.prettify())
    # print(image_link)

    # Go to the page where we can get the full image
    browser.visit(image_link)

    # Delay so we can finish reading the page
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the image tag with the main image and build the final link to the image
    full_image_snippet = soup.find("img", class_="main_image")
    full_image_link = url.split("/spaceimages")[0] + full_image_snippet["src"]

    # print(full_image_link)

    # Quit the browser after scraping
    browser.quit()

    # Return results
    return full_image_link

#
# Go to https://space-facts.com/mars/ and use Pandas scrape the the embedded tables
#


def pandas_scrape_mars_facts():

    # Set the URL to scrape
    pandas_url = "https://space-facts.com/mars/"

    # Read in all the tables from the html page
    tables = pd.read_html(pandas_url)

    # First table contains the information we wants
    mars_df = tables[0]

    # Align the columns and index to the desired output
    mars_df = mars_df.rename(columns={
                             mars_df.columns[0]: "Description", mars_df.columns[1]: "Mars"}).set_index("Description")

    # pprint(mars_df.to_html())

    # Strip the newlines
    html_table = mars_df.to_html(classes="table table-striped")
    html_table = html_table.replace('\n', '')

    # format nicely
    soup = bs(html_table, "html.parser")
    html_table = soup.prettify()

    return html_table

#
# Calls all the scraping functions and returns a dictionary
#


def scrape():

    news = scrape_mars_news()
    featured_image_url = scrape_mars_featured_image()
    mars_facts_table = pandas_scrape_mars_facts()

    return {
        "news": news,
        "featured_image_url": featured_image_url,
        "mars_facts_table": mars_facts_table,
    }
