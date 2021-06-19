# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    news_html = browser.html
    soup_news = bs(news_html, "html.parser")

    # Get News title and news paragraph
    news_title = soup_news.find('div', class_='content_title').text
    news_p = soup_news.find('div', class_="article_teaser_body").text 

    # Assign link to url for JPL Mars Space Images
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    
    # setup Soup for JPL Mars Space Images
    jpl_html = browser.html
    soup_jpl = bs(jpl_html, "html.parser")

    # Scrape page - Img link - into soup 
    jpl_img = soup_jpl.find_all('img')[2]['src']
    featured_image_url = jpl_url+jpl_img

    # Assign link to url for Mars Facts
    mars_facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_facts_url)

    # setup Soup for Mars Facts
    mars_facts_html = browser.html
    soup_mars_facts = bs(mars_facts_html, "html.parser")

    # Scrape sidebar table into soup
    side_bar = soup_mars_facts.find('div', class_='sidebar')
    facts_tbl = side_bar.find_all("tr")

    # read sibe bar tale into pandas dataframe
    facts_tbl_df = pd.read_html(str(side_bar))
    mars_fact_tb_df = facts_tbl_df[0]
    
    # clean up table
    mars_fact_tb_df.columns = ['Mars Profile','Mars Facts']
    mars_fact_tb_df.set_index('Mars Profile')
    
    # convert pandas df into html
    facts_html = mars_fact_tb_df.to_html()
    facts_html.replace('\n','')
    
    # Assign link to url for Mars Hemispheres
    Hemispheres_url = "https://marshemispheres.com/"
    browser.visit(Hemispheres_url)
    
    # setup Soup for Mars Hemispheres
    Hemispheres_html = browser.html
    soup_Hemispheres = bs(Hemispheres_html, "html.parser")
    
    # Stepping into mars hemisphere html to get to div with images 
    hem_mars = soup_Hemispheres.find('div',class_='collapsible results')
    hem_mars_class = hem_mars.find_all('div',class_='item')
    hem_img_url = []
    
    # Loop through each hemisphere item
    for item in hem_mars_class:
        # Error handling  and img_src
        try:
        # Extract title
            hem_desc=item.find('div',class_='description')
            title=hem_desc.h3.text

            # Ex tract image url
            hem_href = hem_desc.a['href']
            browser.visit(Hemispheres_url+hem_href)
            html=browser.html
            soup_hem=bs(html,'html.parser')
            img_src = soup_hem.find('li').a['href']
            img_src = Hemispheres_url+img_src
            if (title and img_src):
            # Print results
                print('--------')
                print(title)
                print(img_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':img_src
            }
            hem_img_url.append(hem_dict)
        except Exception as e:
            print(e)  
    
    mars_data={
    "News_title":news_title,
    "News_paragraph":news_p ,
    "Featured_image_url":featured_image_url ,
    "Mars_facts_tbl":facts_html ,
    "Mars_hem_imgs":hem_img_url    
    }
    
    
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
