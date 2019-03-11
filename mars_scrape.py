from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
import os
from time import sleep

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # hold the results
    scrape_results = {}

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    
    soup = bs(response.text, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    scrape_results['news_title'] = news_title
    news_p = soup.find('div', class_='article_teaser_body')
    scrape_results['news_p'] = news_p
    
    # Nasa's featured image scraping
    
    browser = init_browser()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Navigate to the page with the full, large image
    browser.click_link_by_id('full_image')
    sleep(5)
    browser.click_link_by_partial_text('more info')
    sleep(5)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = soup.find('img').get('src')
    base_url = "https://www.jpl.nasa.gov/spaceimages"
    
    featured_img_url = base_url + image_url
    scrape_results['featured_img_url'] = featured_img_url
    
    # Mars weather report scraping from Twitter
    
    twitter_wx_url = "https://twitter.com/marswxreport?lang=en"
    tweet_response = requests.get(twitter_wx_url)

    tweet_soup = bs(tweet_response.text, 'html.parser')
    mars_weather = tweet_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    scrape_results['mars_weather'] = mars_weather
    
    # Mars Facts scrape
    
    mars_facts_url = "http://space-facts.com/mars/"
    sleep(3)  
    mars_table = pd.read_html(mars_facts_url) 
    mars_facts_df = mars_table[0]
    
    html_table = mars_facts_df.to_html()
    scrape_results['html_table'] = html_table
    
    ### Mars Hemispheres
    
    base_url = "https://astrogeology.usgs.gov/"
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')
    sleep(3)
    image_urls = []
    items = hemi_soup.findAll('div', class_='item')

    for item in items:
        img_url_dict = {'title': [], 'img_url': [],}
        title = item.find('h3').text
        #print(img_url_dict)
        
        hemi_img_url = browser.find_link_by_partial_text('Sample')['href']
        img_url_dict = {'title': title, 'img_url': hemi_img_url}
        #print(image_urls)
        image_urls.append(img_url_dict)
        
        scrape_results['hemi_image_url'] = hemi_img_url
    
    return scrape_results