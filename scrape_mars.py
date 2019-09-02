#!~/anaconda3/envs/pythondata/bin/python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
import lxml
import os
from time import sleep


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/)
    # and collect the latest News Title and Paragraph Text.
    url = "https://mars.nasa.gov/news/"
    driver = webdriver.Chrome()
    driver.get(url)
    # Create BeautifulSoup object find elements
    soup = bs(driver.page_source, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    driver.close()

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and
    # assign the url string to a variable called `featured_image_url`.
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    # Navigate to the page with the full, large image
    browser.click_link_by_id("full_image")
    sleep(2)
    # browser.click_link_by_partial_text("more info")
    # sleep(3)
    html = browser.html
    soup = bs(html, "html.parser")
    # soup.find("div", id="fancybox-lock")
    img_url = soup.find("div", id="fancybox-lock").find("img").get("src")
    base_url = "https://www.jpl.nasa.gov"
    featured_img_url = base_url + img_url
    print(featured_img_url)

    ### Mars Weather
    # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en)
    # Scrape the latest Mars weather tweet from the page.
    # Save the tweet text for the weather report as a variable called `mars_weather`.
    twitter_wx_url = "https://twitter.com/marswxreport?lang=en"
    tweet_response = requests.get(twitter_wx_url)
    tweet_soup = bs(tweet_response.text, "html.parser")
    mars_weather = tweet_soup.find(
        "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
    ).text

    ### Mars Facts
    # Visit the Mars Facts webpage [here](http://space-facts.com/mars/)
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url = "http://space-facts.com/mars/"
    sleep(3)
    mars_table = pd.read_html(mars_facts_url)
    mars_facts_df = mars_table[0]
    # Convert the data to a HTML table string.
    mars_facts_html = mars_facts_df.to_html(table_id="")
    # print(mars_facts_html.translate({ord('\n'): None}))

    ### Mars Hemispheres
    # Visit the USGS Astrogeology site [here]:
    # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar's hemispheres.
    base_url = "https://astrogeology.usgs.gov/"
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")
    # Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # Append the dictionary with the image url string and the hemisphere title to a list.
    # This list will contain one dictionary for each hemisphere.
    hemisphere_img_urls = []
    items = hemi_soup.findAll("div", class_="item")
    # Save both the image url string for the full resolution hemisphere image,
    # and the Hemisphere title containing the hemisphere name.
    for item in items:
        title = item.find("h3").text
        # Click each of the links to the hemispheres in order to find the image url to the full resolution image.
        browser.click_link_by_partial_text("Hemisphere Enhanced")
        browser.windows.current
        hemi_img_soup = bs(browser.html, "html.parser")
        hemi_img_full = hemi_img_soup.find("div", class_="downloads")
        hemi_img_url = hemi_img_full.find("a").get("href")
        hemi_dict = {"title": title, "image_url": hemi_img_url}
        hemisphere_img_urls.append(hemi_dict)
    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_img_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html,
        "hemisphere_image_urls": hemisphere_img_urls,
    }
    return mars_data
