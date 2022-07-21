# THIS IS FOLLOWING THESE INSTRUCTIONS: https://www.youtube.com/watch?v=AS01VoC9l5w

# i think i only need the following 4 lines if im testing ??? i can run:
    # 'python manage.py shell < application.py' 
# from /retail_alerts, and it runs without the following 4 lines.

# # start testing
# import os
# import django

# from retail_alerts.settings import AUTH_TOKEN

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_alerts.settings')
# django.setup()
# #/ end testing

from bs4 import BeautifulSoup
import requests
import validators

#1 color and size out of stock, regular page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=1966&sz=4'

#2 color and size in stock, regular page
# quote_page='https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=31382&sz=4'

#3 color and size out of stock, MD page
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=7218&sz=4'

#4 color and size in stock, MD page -- THIS ONE hAS "HURRY ALMOST OUT OF STOCK"
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=51039&sz=4'

#5 ccolor and lenght selected but no size selected, regular page
# quote_page = 'https://shop.lululemon.com/p/women-crops/Wunder-Train-HR-Crop-21/_/prod9750624?color=26083'

# troubleshooting
quote_page = 'https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=51039&sz=4'

# Get all product details
def get_product_details(quote_page):
    r = requests.get(quote_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    d = {}
    product_name_box = soup.find('div',attrs={'itemprop':'name'})
    try:
        product_name = product_name_box.text.strip()
        d['name'] = product_name
        d['color'] = get_color(quote_page)
        d['size'] = get_size(quote_page)
        price_currency = price(quote_page)
        d['in_stock'] = stock_status(quote_page)
        d['price'] = price_currency['price']
        d['currency'] = price_currency['currency']
        d['url'] = quote_page
        print(d)
        return d
    except AttributeError:
        print(d)
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
    # set defaults for exception handling
    price_currency['price'],price_currency['currency'] = 0,'USD'
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
                        return price_currency # a price wasn't selected, its a range
                    price_currency['price'] = (price.split()[0])[1:]
                    price_currency['currency'] = price.split()[1]
                    return price_currency
        else:
            # regular page
            for p in price:
                price = p.text.strip()
                if '-' in price:
                    return price_currency # a price wasn't selected, its a range
                price_currency['price'] = (price.split()[0])[1:]
                price_currency['currency'] = price.split()[1]
                return price_currency
    except:
        Exception
        return price_currency

def get_photo(quote_page):
    r=requests.get(quote_page)
    soup = BeautifulSoup(r.text,'html.parser')
    # image = ''
    try: 
        image = ''
        images = soup.picture.img['srcset']
        for i in images:
            if i == ' ':
                break
            image = image + i
    except:
        None
        try:
            photo = soup.find_all('img',attrs={'data-testid':'not-lazy-image'})
            links = photo['srcset']
            for l in links:
                if l == ' ':
                    break
                image=image+(l)
        except:
            None
            return None
    if not validators.url(image):
        return None
    return image
