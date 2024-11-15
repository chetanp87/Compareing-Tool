from bs4 import BeautifulSoup
import requests
import random

class ProductScraper:
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    ]

    def __init__(self, query):
        self.query = query
        self.products = []

    def scrape(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_random_user_agent(self):
        return random.choice(self.user_agents)


class AmazonScraper(ProductScraper):
    def scrape(self):
        url = "https://www.amazon.in/s?k=" + self.query
        headers = {'User-Agent': self.get_random_user_agent(), 'Accepted-Language': 'en-US, en;q=0.5'}
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")

        sections = soup.find_all("div", attrs={'class': 'sg-col-inner'})
        
        for div in sections:
            product_info = {}
            #name of product
            name = div.find('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
            if name is not None:
                product_info['name'] = name.get_text()
            else:
                continue

            #price of product
            price = div.find('span', attrs={'class': 'a-offscreen'})
            if price is not None:
                product_info['price'] = price.get_text()
            else:
                continue

            #rating of product
            rating = div.find('span', attrs={'class': 'a-icon-alt'})
            if rating is not None:
                stars = rating.get_text()
                product_info['rating'] = stars[:4]
            else:
                continue

            #product link
            link_to_product = div.find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            link_to_product = "https://www.amazon.in" + link_to_product.get('href')
            if "www.amazon.inhttps" in link_to_product:
                continue
            else:
                product_info['link'] = link_to_product

            #image link
            image_tag = div.find('img', attrs={'class': 's-image'})
            if image_tag:
                product_info['image'] = image_tag['src']
            else:
                continue

            if product_info:
                # print("i am not going in digital")
                self.products.append(product_info)
        if self.products:
            return
        else:
            self.amdigital()

    def amdigital(self):
        url = "https://www.amazon.in/s?k=" + self.query
        headers = {'User-Agent': self.get_random_user_agent(), 'Accepted-Language': 'en-US, en;q=0.5'}
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        print("in amazon digital ")
        sections = soup.find_all("div",attrs={'class':'sg-col-inner'})
        # print(sections)

        for div in sections:
            product_info = {}
            #name of product
            name = div.find('span',attrs={'class':'a-size-medium a-color-base a-text-normal'})
            
            if name is not None:
                product_info['name'] = name.get_text()
                # print(name.get_text())
            else:
                continue
        
            #price of product
            price = div.find('span',attrs={'class':'a-offscreen'})
            if price is not None:
                product_info['price'] = price.get_text()
            else:
                continue

            #rating of product
            rating = div.find('span',attrs={'class':'a-icon-alt'})
            if rating is not None:
                stars = rating.get_text()
                product_info['rating'] = stars[:4]
                
            else:
                continue

            #product link
            link_to_product=div.find('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            link_to_product = link_to_product.get('href')
            link_to_product = "https://www.amazon.in" + link_to_product
            if "www.amazon.inhttps" in link_to_product:
                print("link corrupted")
                continue
            else:
                product_info['link'] = link_to_product
            
            #image link
            image_tag = div.find('img',attrs={'class':'s-image'})
            if image_tag:
                product_info['image'] = image_tag['src']
            
            else:
                continue

            if product_info:
                self.products.append(product_info)

class FlipkartScraper(ProductScraper):
    def scrape(self):
        print("In flipkart")
        url = "https://www.flipkart.com/search?q=" + self.query
        headers = {'User-Agent': self.get_random_user_agent()}
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")

        sections = soup.find_all("div", attrs={'data-id': True})
        
        for div in sections:
            product_info = {}
            #name of product
            name = div.find('a', attrs={'class': 'wjcEIp'})
            if name is None:
                name = div.find('a', attrs={'class': 'WKTcLC'})
            if name is not None:
                product_info['name'] = name.get('title')
            else:
                continue

            #price of product
            price = div.find('div', attrs={'class': 'Nx9bqj'})
            if price is not None:
                product_info['price'] = price.get_text()
            else:
                continue

            #rating of product
            rate = div.find('div', attrs={'class': 'XQDdHH'})
            if rate is not None:
                product_info['rating'] = rate.get_text()
            else:
                product_info['rating'] = 4

            #product link
            link_to_product = "https://www.flipkart.com" + name.get('href')
            if "https://www.flipkart.comhttps" in link_to_product:
                continue
            else:
                product_info['link'] = link_to_product

            #image link
            image_tag = div.find('img')
            if image_tag:
                product_info['image'] = image_tag['src']
            else:
                continue

            self.products.append(product_info)
        self.flipdigital()

    def flipdigital(self):
        url = "https://www.flipkart.com/search?q=" + self.query
        headers = {'User-Agent': self.get_random_user_agent()}
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        sections = soup.find_all("a", attrs={'class': 'CGtC98'})
        for div in sections:
            product_info = {}
            #name of product
            name = div.find('div',attrs={'class':'KzDlHZ'})
            if name is not None:
                product_info['name'] = name.get_text()
            else:
                continue
        
            #price of product
            price = div.find('div',attrs={'class':'Nx9bqj _4b5DiR'})
            if price is not None:
                product_info['price'] = price.get_text()
            
            else:
                continue

            #rating of product
            rate = div.find('div',attrs={'class':'XQDdHH'}) #XQDdHH
            if rate is not None:
                product_info['rating'] = rate.get_text()
            
            else:
                product_info['rating'] = 4

            #product link
            link_to_product = div.get('href')
            link_to_product = "https://www.flipkart.com" + link_to_product
            
            if "https://www.flipkart.comhttps" in link_to_product:
                print("link corrupted")
                continue
            else:
                product_info['link'] = link_to_product
            
            
            #image link
            image_tag = div.find('img')
            if image_tag:
                product_info['image'] = image_tag['src']
                # print(product_info['image'])
            
            else:
                continue
        
            self.products.append(product_info)


