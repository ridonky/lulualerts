from django.test import TestCase

# Create your tests here.


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
# quote_page = 'https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket-MD/_/prod8240067?color=24921&sz=4'

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
