# Mission To Mars

**_Mission To Mars_** - In this exercise the purpose is to scrape the given Mars web pages to pull news, images, and information for Mars. This code demonstrates how to use the package Beautiful Soup to walk through the HTML DOM and find specific elements on each page. Then we use MongoDB to store the results of the scraping so that it later can be retrieved and displayed by a Flask application via a template.

## Files

- [mission_to_mars.ipynb](mission_to_mars.ipynb) - Jupyter Notebook that was used to experiment with the screen scraping

- [scrape_mars.py](scrape_mars.py) - Translation of the Jupyter Notebook code into a python module to be used by a Flask application to display the Mars data

- [app.py](app.py) - The main Flask app that serves two routes **/** and **/scrape**, the first route reads from MongoDB and displays the content and the second scrapes the Mars web pages and stores it into MongoDB

- [index.html](templates/index.html) - The HTML template used by Flask used to display the data

- [style.css](static/style.css) - Some basic styling for the HTML template

- [point_up.png](static/point_up.png) - Default image for pre-scrape screen

- [favicon.ico](static/favicon.ico) - Having some fun with a favicon

## Results

![Top Html](images/top_html.jpg)
![Top Html](images/middle_html.jpg)
![Top Html](images/bottom_html_1.jpg)
![Top Html](images/bottom_html_2.jpg)

## Execution

1. The assumption is that you have a working Python 3.6 environment and:

   - Jupyter Notebook 6.1.4
   - pandas 1.0.5
   - Flask 1.1.2
   - Flask-PyMongo 2.3.0
   - splinter 0.14.0
   - beautifulsoup4 4.9.3

1. You will need download [_chromedriver.exe_](https://chromedriver.chromium.org/downloads) (or Mac OS equivalent for Mac) and ensure it is on your PATH. This will be executed by splinter during your screen scraping. If you have any trouble _make sure_ the version of your `chromedriver.exe` matches you Chrome browser version (87 <-> 87)
1. Ensure you have a MongoDB up and running on your localhost (default port with no login restrictions)
1. Clone the [git repository](https://github.com/jayhjman/web-scraping-challenge) for this project
1. Change into the repository directory
1. Execute the `app.py` file by typing `python app.py`
1. Open up Chrome and go to http://localhost:5000/

## Author

Made by [Jay](https://www.linkedin.com/in/jay-hastings-techy/) with :heart: in 2020.
