
def scrape():
    import pandas as pd
    from splinter import Browser
    from bs4 import BeautifulSoup

    #### Scrape NASA Mars News Site and collect latest 
    #### News Title and Paragraph Text.

    # Perform HTML Scrape via splinter and BeautifulSoup
    browser = Browser('chrome', headless=False)
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')
    browser.quit()

    # Eliminate unwanted text using BeautifulSoup
    title = soup1.find('div', class_='content_title')
    news_title = str(title).split('elf">')[1].split('</a>')[0]
    news = soup1.find('div', class_='article_teaser_body')
    news_p = str(news).split('ody">')[1].split('</div')[0]

    #### Scrape NASA Jet Propulsion Lab's martian website
    #### for latest featured image. 
    browser = Browser('chrome', headless=False)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    browser.quit()

    # Eliminate unwated text using BeautifulSoup
    featured_image = soup2.find('div', class_='carousel_items')
    featured_image_url = "https://www.jpl.nasa.gov/" + str(featured_image).split("url('/")[1].split("');")[0]


    #### Scrape the Mars Weather twitter account for the most recent
    #### martian weather.
    browser = Browser('chrome', headless=False)
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    browser.quit()


    # Isolate tweet text and check to ensure that the tweet does indeed contain
    # martian weather information. 
    weather = soup3.findAll("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    tweet_list = []
    mars_weather = ""
    for data in weather:
        tweet_list.append(str(data))
    for data in tweet_list:
        if data.split('="en">')[1].split('</p>')[0].startswith("Sol") == True:
            mars_weather = data.split('="en">')[1].split('</p>')[0]
            break
        else:
            pass




    #### Scrape Mars facts table and export it to a html table using pandas.
    mars_facts_df = pd.read_html('https://space-facts.com/mars/')
    mars_facts_df[0].to_html('mars_facts.html', header=False)



    #### Scrape the USGS Astrogeology website for Martian Hemisphere images and
    #### titles.
        
    browser = Browser('chrome', headless=False)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')

    hemispheres = soup4.findAll('div', class_='description')
    browser.quit()

    #Loop through initial links to find download links.

    hemisphere_links = []
    for sphere in hemispheres:
        hemisphere_links.append('https://astrogeology.usgs.gov' + str(sphere).split('href="')[1].split('"><h3>')[0])

    #Loop through download landing pages and search for download links and titles.

    hemisphere_image_urls = []

    for link in hemisphere_links:
        browser = Browser('chrome', headless=False)
        browser.visit(link)
        htmlx = browser.html
        soupx = BeautifulSoup(htmlx, 'html.parser')
        tempx = soupx.findAll("div", class_="content")    
        hemisphere_image_urls.append({
                "title" : str(tempx).split('"title">')[1].split(' Enhanced<')[0],
                "img_url" : str(tempx).split('Filename</dt><dd><a href="')[1].split('">')[0]
            })
        browser.quit()
    scrape_mars_dict = {
        "data" : True,
        "featured_image_url" : featured_image_url,
        "news_title" : news_title,
        "news_p" : news_p,
        "mars_weather" : mars_weather,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    return(scrape_mars_dict)
