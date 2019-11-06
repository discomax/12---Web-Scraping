# Mission to Mars

![mission_to_mars](Images/mission_to_mars.jpg)

This is a small a web application that scrapes various websites for data related to the planet Mars and displays the information in a single HTML page. 

## Web Scraping

Scraped using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

### NASA Mars News

* Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.

### JPL Mars Space Images - Featured Image

* Scraped the JPL Featured Space Image from [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Made sure to find the image url to the full size `.jpg` image.

```python
# Example:
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
```

### Mars Weather

* Using the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) , scraped the latest Mars weather tweet from the page.

```python
# Example:
mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
```

### Mars Facts

* From the Mars Facts webpage [here](http://space-facts.com/mars/), used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Converted the data to a HTML table string.

### Mars Hemispheres

* Scraped the high resolution images for each of Mar's hemispheres from thebUSGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars).

* Assigned each image url string and hemisphere title to a dictionary and appended each dict. to a list. 

```python
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]
```

- - -

## MongoDB and Flask Application

Created a HTML page with FLASK template to display all of the Mars information which I stored in a MongoDB.

* Converted the Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of the scraping code and return a Python dictionary containing all of the data.

* Made a route called `/scrape` to import the `scrape_mars.py` script and call the `scrape` function.

  * Returns value in Mongo as a Python dictionary.

* Root route `/` queries Mongo db then passes data into an HTML template for displaying.

* Created`index.html` to take the mars data dictionary and display all of the data in the appropriate HTML elements.

![final_app_part1.png](Images/final_app_part1.png)
![final_app_part2.png](Images/final_app_part2.png)

- - -

## Designed by Michael Patterson
