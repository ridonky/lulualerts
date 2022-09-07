from bs4 import BeautifulSoup
import requests
import validators

# Get all product details
def get_product_details(quote_page):
    request = requests.get(quote_page)
    soup = BeautifulSoup(request.text, 'html.parser')
    details = {}
    product_name_box = soup.find('div',attrs={'itemprop':'name'})
    try:
        # color
        details['color'] = get_color(quote_page)
        # size
        details['size'] = get_size(quote_page)
        # price & currency
        price_currency = price(quote_page)
        details['price'] = price_currency['price']
        details['currency'] = price_currency['currency']
        # stock status
        details['in_stock'] = stock_status(quote_page)
        # url
        details['url'] = quote_page
        # product name
        product_name = product_name_box.text.strip()
        details['name'] = product_name
        return details
    except AttributeError:
        return details

def get_color(quote_page):
    request = requests.get(quote_page)
    soup = BeautifulSoup(request.text,'html.parser')
    color2 = soup.find('span',attrs={'class':'color-selection_colorNameValue__3m_yW'}).text
    return color2

def get_size(quote_page):
    request=requests.get(quote_page)
    soup = BeautifulSoup(request.text,'html.parser')
    size2 = soup.find('div',attrs={'class':'purchase-attribute-carousel-counter_purchaseAttributeCarouselCounter__WpivI'})
    for child in size2.descendants:
        if 'Size' in child.text:
            continue
        else:
            size = child.text
            return size

def stock_status(quote_page):
    request=requests.get(quote_page)
    soup = BeautifulSoup(request.text,'html.parser')
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
    request = requests.get(quote_page)
    soup = BeautifulSoup(request.text, 'html.parser')
    try:
        price = soup.find('span', attrs={'class':'price-1jnQj'}).find_all('span')
        # MD page
        if len(price) > 1:
            for pricedata in price:
                if pricedata['class'] == []:
                    price = pricedata.text.strip()
                    if '-' in price:
                        return price_currency # a price wasn't selected, its a range
                    price_currency['price'] = (price.split()[0])[1:]
                    price_currency['currency'] = price.split()[1]
                    return price_currency
        else:
            # regular page
            for pricedata in price:
                price = pricedata.text.strip()
                if '-' in price:
                    return price_currency # a price wasn't selected, its a range
                price_currency['price'] = (price.split()[0])[1:]
                price_currency['currency'] = price.split()[1]
                return price_currency
    except:
        Exception
        return price_currency

def get_photo(quote_page):
    request=requests.get(quote_page)
    soup = BeautifulSoup(request.text,'html.parser')
    try: 
        image = ''
        images = soup.picture.img['srcset']
        for imagetext in images:
            if imagetext == ' ':
                break
            image=image+imagetext
    except:
        None
        try:
            photo = soup.find_all('img',attrs={'data-testid':'not-lazy-image'})
            links = photo['srcset']
            for linktext in links:
                if linktext == ' ':
                    break
                image=image+(linktext)
        except:
            None
            return None
    if not validators.url(image):
        return None
    return image