# resources:
# https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/
# zhias docs: https://zhiachong.com/blog/automating-my-job-search-with-python/

from pprint import PrettyPrinter
from bs4 import BeautifulSoup
import os
import requests

#color and size in stock, regular page: 
quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=17441&sz=4'

#color and size out of stock, regular page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=0001&sz=4'

#no selection made, (e.g. - just color) regular page:
# quote_page = ?

#color and size in stock, md page:
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD'

# color and size 
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD?sz=16'


#need to transform the user input to some searched thing?
payload = {'Ntt':'define'}
r2 = requests.get('https://shop.lululemon.com/search', params=payload)
print(r2.url)
print(r2)
print("")
soup = BeautifulSoup(r2.text,'html.parser')
product_list=soup.find_all('div',attrs={'data-testid':'product-list'})
print(f'product_list is {product_list}')
for desc in product_list:
    print(desc)


r = requests.get(quote_page)
# f = open("newfile.txt","w")
# f.write(r.text)
# f.close
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.p)
# print(soup.title.string)
# print(soup.find('div',attrs={'itemprop':'name'}))


#Attributes to scrape:


#Product name
product_name_box = soup.find('div',attrs={'itemprop':'name'})
product_name = product_name_box.text.strip()
print(product_name)

# Selected Size & Selected Color
size_box = soup.find_all('div',attrs={'aria-checked':'true'})
for b in size_box:
    if b.has_attr('aria-label'):
        color = b['aria-label']
    elif b.has_attr('span') != None:
        size = b.text

print(f'selected color is {color}')
print(f'selected size is {size}')










#Price - MD only
# price_box = soup.find('span',attrs={'class':'price-1jnQj price'})
# if price_box.find('span',attrs={'class':'lll-hidden-visually'}).text != None:
#    print("")
#    price = price_box.find('span',attrs={'class':''})
#    print(price.text) 
# print(price_box)

#SKU
# sku_box = soup.find('div', attrs={'class':'product-sku'}).text
# print(sku_box)

# # All Colors
colors_box = soup.find('div',attrs={'class':'color-selection_colorSelector__E6oWb'})

# print(colors_box)


for child in colors_box.descendants:
    if child.get('aria-label') and child.get('role') == 'radio':
            print(child['aria-label'])
    else:
        continue
    # print("NEXTKID")
    # print(child)
    # if child.find('div',attrs={'aria_label'}):
    #     colors.append(child.div['aria_label'])
    # else:
    #     continue
# print(colors_box.div.children)


# colors = []
# for div in colors_box.find_all('div'):
#     print(div)
#     print("")
#     print("nextdivbaby")
#     print("")

#     color = colors_box.div['aria_label']
#     if color:
#         colors.append(color)
#     else:
#         continue