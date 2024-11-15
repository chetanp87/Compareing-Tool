from bs4 import BeautifulSoup
import requests
import csv
import random
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
]
# import time

HEADERS = ({'User-Agent' : random.choice(user_agents),
            'Accepted-Language' : 'en-US, en;q=0.5'})

def amazon_products(query,am_products):
    URL= "https://www.amazon.in/s?k=" 
    URL += query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")


    sections = soup.find_all("div",attrs={'class':'sg-col-inner'})
    # print("in here")
    for div in sections:
        product_info = {}
        #name of product
        name = div.find('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
        if name is not None:
            product_info['name'] = name.get_text()
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
            am_products.append(product_info)
    if am_products:
        return
    else:
        amazon_digital(query,am_products)


def amazon_digital(query, am_products):
    URL= "https://www.amazon.in/s?k=" 
    URL += query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")

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
            am_products.append(product_info)


def flipkart_products(query,flip_products):
    
    URL = "https://www.flipkart.com/search?q=" + query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")

    sections = soup.find_all("div", attrs={'data-id': True})
    
    for div in sections:
        product_info = {}
        #name of product
        name = div.find('a',attrs={'class':'wjcEIp'})#   slAVV4 
        if name is None:
            name = div.find('a',attrs={'class':'WKTcLC'})#   slAVV4 
            # print("name of type 2")
            # print(name)
        # print(name)
        if name is not None:
            product_info['name'] = name.get('title')
            # print(name.get('title'))
        else:
            continue
    
        #price of product
        price = div.find('div',attrs={'class':'Nx9bqj'})
        if price is not None:
            product_info['price'] = price.get_text()
        
            # print(price.get_text())
        else:
            continue

        #rating of product
        rate = div.find('div',attrs={'class':'XQDdHH'}) #XQDdHH
        if rate is not None:
            product_info['rating'] = rate.get_text()
        
            # print(rate.get_text())
        else:
            product_info['rating'] = 4

        #product link
        link_to_product = name.get('href')
        link_to_product = "https://www.flipkart.com" + link_to_product
        # print(link_to_product)
        if "https://www.flipkart.comhttps" in link_to_product:
            print("link corrupted")
            continue
        else:
            product_info['link'] = link_to_product
        
        #image link
        image_tag = div.find('img')
        if image_tag:
            product_info['image'] = image_tag['src']
        
        else:
            continue
    
        flip_products.append(product_info)
    if flip_products:
        return
    else:
        flip_digital(query,flip_products)

def flip_digital(query,flip_products):
    print("in flipkart digital")
    URL = "https://www.flipkart.com/search?q=" + query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")

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
    
        flip_products.append(product_info)