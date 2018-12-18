from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import pymongo

# Initialize browser
def init_browser():
   #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
   executable_path = {'executable_path': 'chromedriver.exe'}
   return Browser("chrome", **executable_path, headless=False)


# Function to scrape for space data
def scrape():

   # Initialize browser
   #  browser = init_browser()

   browser = Browser('chrome')
   mars = {}

   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")

   # MARS news header and news body
   article = soup.find("div", class_='list_text')
   mars["news_title"] = article.find("div", class_="content_title").text
   mars["news_p"] = article.find("div", class_="article_teaser_body").text

          
   # Image of the MARS page 
   image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(image_url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")

   image = soup.find('a', class_= 'button fancybox')['data-fancybox-href']
   mars["feature_img"] = 'https://www.jpl.nasa.gov' + image
    
   # Data from the twitter Feed
   twit_url = "https://twitter.com/marswxreport?lang=en"
   response = requests.get(twit_url)
   soup = BeautifulSoup(response.text, 'html.parser')
   mars["mars_weather"] = soup.find_all('p')[5].get_text()

   # #Mars Facts 
   
   
   url = 'http://space-facts.com/mars/'
   marsfacts = pd.read_html(url)

   # Using .rename(columns={}) in order to rename columns
   marsfacts_df = marsfacts[0]
   renamed_marsfacts_df = marsfacts_df.rename(columns={0:"Facts", 1:"Value"})

   #mars_facts=mars_facts.set_index('description')
   renamed_marsfacts_df1 = renamed_marsfacts_df.set_index('Facts')
   
   #Convert df to html table string
   marsfacts_html=renamed_marsfacts_df.to_html()
   #mars["mars_facts"]=renamed_marsfacts_df1
   
   # for loop to get all data elements in an array
   hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   browser.visit(hemispheres_url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   mars_hemisphere = []

   products = soup.find("div", class_ = "collapsible results" )
   hemispheres = products.find_all("div", class_="item")

   for hemis in hemispheres:
      title = hemis.find("h3").text
      title = title.replace("Enhanced", "")
      link = hemis.find("a")["href"]
      img_link = "https://astrogeology.usgs.gov/" + link    
      browser.visit(img_link)
      html = browser.html
      soup=BeautifulSoup(html, "html.parser")
      downloads = soup.find("div", class_="downloads")
      image_url = downloads.find("a")["href"]
      mars_hemisphere.append({"title": title, "img_url": image_url})

      mars["mars_hemisphere"]=mars_hemisphere
   

   return mars



