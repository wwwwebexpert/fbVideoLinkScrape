from selenium import webdriver
from bs4 import BeautifulSoup

class fbVideoLinkScrapper(object):

    def __init__(self, url, page_source, browserObj):
        self.url = url
        self.page_source = page_source
        self.browserObj = browserObj

    def convertToInt(self, value):
        if type(value) == float or type(value) == int:
            return value
        elif 'K' in value:
            return int(value.replace('K', '')) * 1000    
        elif 'M' in value:
            return int(value.replace('M', '')) * 1000000
        elif 'B' in value:
            return int(value.replace('B', '')) * 1000000000
        else:
            return int(value)    

    def scrape_item(self):
        """
        This method actually retrieves the data form the item itself

        Remember to log:

        - That you started scraping this single item
        - If any fields were not found
        - If the request failed
        - That the json was sent to the processor
        - Any unexpected behavior
        """

        # Log that the individual scraping begins
        
        print('Scraping %s' % self.url)
        
        soup = BeautifulSoup(self.page_source,"html.parser")
        
        article_leftpanel = soup.find('div', {'id':'stream_pagelet'})

        internal_section = article_leftpanel.find('form')

       

        #print(get_views.prettify())

        result = {}

        views = None
        likes = None
        shares = None
        comments = None
        

        try:
            viewString = internal_section.find('span',{'class':'fcg'}).getText()
            if(viewString!=''):
                splitViews = viewString.split(' ')
                views = self.convertToInt(splitViews[0])
        except:
            pass

        try:
            viewLikes = internal_section.find('span',{'class':'_2u_j'}).getText()

            if(viewLikes!=''):
                splitLikes = viewLikes.split(' ')
                likes = self.convertToInt(splitLikes[0])
        except:
            pass

        try:
            viewComments = internal_section.find('span',{'class':'_2u_j'}).find_next_sibling().getText()

            if(viewComments!=''):
                splitComments = viewComments.split(' ')
                comments = self.convertToInt(splitComments[0])
        except:
            pass

       


        result = {
            'title': views,
            'likes': likes,
            'comments': comments
        }

        print(result)
       
        self.browserObj.quit()

    def run(self):
        """
        This is the main method. Your scraper should always run like this:
        scraper.run()
        """
        try:
            result = self.scrape_item()
                
        except: # If anything happens to interrupt the scraping: log it
            pass


if __name__ == '__main__':
    url = 'https://www.facebook.com/JungleVT/videos/1720510198003354/'

    browser = webdriver.Firefox()
    browser.get(url)

    scraper = fbVideoLinkScrapper(url,browser.page_source, browser)
    scraper.run()
