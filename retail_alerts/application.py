# THIS IS FOLLOWING THESE INSTRUCTIONS: https://www.youtube.com/watch?v=AS01VoC9l5w

# i think i only need the following 4 lines if im testing ??? i can run:
    # 'python manage.py shell < application.py' 
# from /retail_alerts, and it runs without the following 4 lines.

# start testing
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_alerts.settings')
django.setup()
#/ end testing

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit
import requests
# from django.contrib.auth.models import User
from lulu_alerts.models import Products, Alerts, Alert_Status


#1 color and size out of stock, regular page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=1966&sz=4'

#2 color and size in stock, regular page
# quote_page='https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=31382&sz=4'

#3 color and size out of stock, MD page
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=7218&sz=4'

#4 color and size in stock, MD page -- THIS ONE hAS "HURRY ALMOST OUT OF STOCK"
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=51039&sz=4'


# Get all product details
def get_product_details(quote_page):
    r = requests.get(quote_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    d = {}
    product_name_box = soup.find('div',attrs={'itemprop':'name'})
    product_name = product_name_box.text.strip()
    d['name'] = product_name
    d['color'] = get_color(quote_page)
    d['size'] = get_size(quote_page)
    price_currency = price(quote_page)
    d['in_stock'] = stock_status(quote_page)
    d['price'] = price_currency['price']
    d['currency'] = price_currency['currency']
    d['url'] = quote_page
    return d

def get_color(quote_page):
    r = requests.get(quote_page)
    soup = BeautifulSoup(r.text,'html.parser')
    color2 = soup.find('span',attrs={'class':'color-selection_colorNameValue__3m_yW'}).text
    return color2

def get_size(quote_page):
    r=requests.get(quote_page)
    soup = BeautifulSoup(r.text,'html.parser')
    size2 = soup.find('div',attrs={'class':'purchase-attribute-carousel-counter_purchaseAttributeCarouselCounter__WpivI'})
    for child in size2.descendants:
        if 'Size' in child.text:
            continue
        else:
            size = child.text
            return size

def stock_status(quote_page):
    r=requests.get(quote_page)
    soup = BeautifulSoup(r.text,'html.parser')
    stock = soup.find(id='purchase-attributes-size-notification-error')
    if stock == None:
        return True
    else: #its out of stock
        return False

# Get item price
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
                    if '-' in price:
                        return None # a price wasn't selected, its a range
                    price_currency['price'] = (price.split()[0])[1:]
                    price_currency['currency'] = price.split()[1]
                    return price_currency
        else:
            # regular page
            for p in price:
                price = p.text.strip()
                if '-' in price:
                    return None # a price wasn't selected, its a range
                price_currency['price'] = (price.split()[0])[1:]
                price_currency['currency'] = price.split()[1]
                return price_currency
    except:
        Exception
        print("couldn't get product details.. try again")
        return None

# URL Processer: normalizes user provided URL into 2 urls to get for sale pages
def urls_alt(quote_page):
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


# Scheduled check for alert trigger
def alerts_check():
    active = Alerts.objects.filter(status=1) 
    price_drop_alerts = active.filter(alert_type = "price_drop")
    price_drop_check(price_drop_alerts)
    #continue writing this for back in stock alerts

def price_drop_check(alerts):
    for alert in alerts:
        # get the target price
        # get the urls
        dburl = alert.product.url
        url = confirm_url(dburl,alert.product)
        target_price = alert.target_price
        pricecheck = price(url)
        if pricecheck['currency'] == alert.product.currency:
            if pricecheck['price'] <= target_price:
                # send an alert!
                pass
            else:
                # check the next alert. or maybe shoudl check the next url
                continue
        else:
            # currency is wrong... handle this.
            pass


# return the right url to look for for a particular product.
def confirm_url(url,product):
    p = get_product_details(url)
    if p['color'] != product.color or p['size'] != product.size:
        alt = urls_alt(url)
        if get_size(alt['md']) == product.size and get_color(alt['md']) == product.color:
            return alt['md']
        elif get_size(alt['url']) == product.size and get_color(alt['md']) == product.color:
            return alt['url']
        else:
            return None
    else:
        return url
    # all product details are on the product page its the right url, else process it

