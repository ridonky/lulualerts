from bs4 import BeautifulSoup
import requests
import validators
# WORKS
#1 color and size out of stock, regular page:
#quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=1966&sz=4'

# WORKS
#2 color and size in stock, regular page
# quote_page='https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=31382&sz=4'

# DOESNT WORK
#3 color and size out of stock, MD page
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=7218&sz=4'

# DOESNT WORK
#4 color and size in stock, MD page -- THIS ONE hAS "HURRY ALMOST OUT OF STOCK"
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=51039&sz=4'

# WORKS
#5 ccolor and lenght selected but no size selected, regular page
# quote_page = 'https://shop.lululemon.com/p/women-crops/Wunder-Train-HR-Crop-21/_/prod9750624?color=26083'

# WORKS
# tester
# quote_page = 'https://shop.lululemon.com/p/tops-short-sleeve/Cates-Tee/_/prod9271065?color=40036&sz=4'

#quote_page = 'https://shop.lululemon.com/p/tops-short-sleeve/Cates-Tee/_/prod9271065?color=40036&sz=4'

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
    print(image)
    return image

get_photo(quote_page)