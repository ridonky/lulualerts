from bs4 import BeautifulSoup
import requests
import validators

#1 color and size out of stock, regular page:
#  quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=1966&sz=4'

#2 color and size in stock, regular page
# quote_page='https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=31382&sz=4'

#3 color and size out of stock, MD page
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=7218&sz=4'

#4 color and size in stock, MD page -- THIS ONE hAS "HURRY ALMOST OUT OF STOCK"
# quote_page='https://shop.lululemon.com/p/women-pants/Align-Pant-2-MD/_/prod8360162?color=51039&sz=4'

#5 ccolor and lenght selected but no size selected, regular page
quote_page = 'https://shop.lululemon.com/p/women-crops/Wunder-Train-HR-Crop-21/_/prod9750624?color=26083'

# invalid
# quote_page='https://validators.readthedocs.io/en/latest/'

def photo(quote_page):
    r=requests.get(quote_page)
    soup = BeautifulSoup(r.text,'html.parser')
    # image = ''
    try: 
        images = soup.picture.img['srcset']
        image = ''
        for i in images:
            if i == ' ':
                break
            image = image + i
    except:
        None
    if not validators.url(image):
        image = 'not a real url'
    print(image)

    # print(soup.picture.img)
    # photo=soup.find('img')


    # print(photo)
    # photo = soup.find_all('img',attrs={'data-testid':'not-lazy-image'})
    # print(photo)
    # links = photo['srcset']
    # print(links)
    # for l in links:
    #     if l == ' ':
    #         break
    #     image=image+(l)
    # # except:
    # #     TypeError    
    # if not validators.url(image):
    #     image = 'not a url'
    # print(image)

photo(quote_page)