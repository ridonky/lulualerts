# resources:
# https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/
# zhias docs: https://zhiachong.com/blog/automating-my-job-search-with-python/

from pprint import PrettyPrinter
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urlunsplit
# https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
import requests
import time

# Quote Page testing:
#color and size in stock, regular page: 
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=17441&sz=4'

#color and size out of stock, regular page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=0001&sz=4'

# item has color = no color; size is not selected
# quote_page = 'https://shop.lululemon.com/p/selfcare/Anti-Stink-Deodorant-Sandalwood-MD/_/prod10730114?color=1426'

#color and size in stock, item page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD'

# color and size 
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD?sz=16'

# regular item, color and size selected, in stock
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=54319&sz=4'

# MD item, color and size selected, in stock
quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD/_/prod8240067?color=24921&sz=4'

# MD item, color selected, no size selected
# quote_page = 'https://shop.lululemon.com/p/women-crops/Swift-Speed-HighRise-Crop-21-MD/_/prod10510180?color=47184'

# mirror
# quote_page = 'https://www.mirror.co/shop/mirror-basic?utm_source=lululemon_site&utm_medium=lululemon&utm_campaign=story_page_atf_shop_cta'

# reg item, color selected, no size selected -
# quote_page = "https://shop.lululemon.com/p/men-joggers/Abc-Jogger-Skinny/_/prod9640028?color=33928"


# all the same item
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket/_/prod5020054?color=54319&sz=2'
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD/?color=54319&sz=2'
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket/?color=54319&sz=2'


#take the 1st 3 path folders from the path
    # if it ends in MD remove MD & save as alt, if doesnt endin md, add and save as alt
# append the query


def get_product_details(quote_page):
    r = requests.get(quote_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    d = {}

    #Product name
    product_name_box = soup.find('div',attrs={'itemprop':'name'})
    product_name = product_name_box.text.strip()
    d['name'] = product_name

    # Selected Size & Selected Color
    size_box = soup.find_all('div',attrs={'aria-checked':'true'})
    for b in size_box:
        if b.has_attr('aria-label'):
            color = b['aria-label']
        elif b.has_attr('span') != None:
            size = b.text

    d['color'] = color
    d['size'] = size

    price_currency = price(quote_page)
    d['price'] = price_currency['price']
    d['currency'] = price_currency['currency']
   
    d['url'] = quote_page # 

    # THIS CAN HAPPEN LATER --- WHEN THE DB IS PINGING ??
    # urls = url_processer(quote_page)
    # print(urls)
    # d['url_regular'] = urls['regular']
    # d['url_md'] = urls['md']
    
    # END FOR TEST ONLY
    
    print(d)
    return d

# Passes all tests - but need to separate price and currency
def price(quote_page):
    price_currency = {}
    r = requests.get(quote_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        price = soup.find('span', attrs={'class':'price-1jnQj'}).find_all('span')
        # MD page
        if len(price) > 1:
            for p in price:
                if p['class'] == []:
                    price = p.text.strip()
                    # MD page - price range
                    if '-' in price:
                        return None
                    price_currency['price'] = (price.split()[0])[1:]
                    price_currency['currency'] = price.split()[1]
                    return price_currency
        else:
            # regular page
            for p in price:
                price = p.text.strip()
                # regular page - price range
                if '-' in price:
                    print('please select a size')
                    return None
                price_currency['price'] = (price.split()[0])[1:]
                price_currency['currency'] = price.split()[1]
                return price_currency
    except:
        Exception
        print("couldn't get product details.. try again")
        return None

# normalizes user provided URL into 2 urls to get for sale pages
def url_processer(quote_page):
    urls={}
    p = urlparse(quote_page)
    cleanpath = p.path.split("_")[0] # removes the sku from the URL if its there
    if "-MD" not in p.path:
        urls["regular"] = urlunsplit((p.scheme,p.netloc,cleanpath,p.query,p.fragment))
        # store the reg url, the add the MD
        cleanpath = cleanpath.removesuffix("/") + "-MD/"
        urls["md"] = urlunsplit((p.scheme,p.netloc,cleanpath,p.query,p.fragment))
    else:
        urls["md"] = urlunsplit((p.scheme,p.netloc,cleanpath,p.query,p.fragment))
        # store the md url, then add the reg
        cleanpath = cleanpath.removesuffix("-MD/") + "/"
        urls["regular"] = urlunsplit((p.scheme,p.netloc,cleanpath,p.query,p.fragment))
    return urls

# url_processer(quote_page)
get_product_details(quote_page)