# lulu alerts
<!-- ![lulualerts logo](retail_alerts/lulu_alerts/static/lulu_alerts/big_icon.png) -->
![homepage gif](readme/homepageloop.gif)

## Project overview
lulu alerts makes sure shoppers don't miss out on purchasing their favorite lululemon products as soon as they go on sale or come back in stock with notifications delivered to their inboxes 

### Description
lulu alerts is a web application for creating and managing alerts for lululemon products.  Users create lulu alerts accounts, where they can configure two types of alerts: (1) "back in stock", which notifies them when an out of stock product comes back in stock, as well as (2) "price drop", which tell them when a particular product decreases in price.  On an ongoing basis, the app monitors lululemon.com to see if any existing alerts should be triggered by a particular product price change or product back in stock.  When an alert is triggered, lulu alerts notifies the user via email. lulu alerts scrapes HTML to grab product attributes such as price, color, size, and product name, from lululemon.com during alert configuration and ongoing alert monitoring.

### Technologies
- Python
- Javascript
- HTML/CSS
- Bootstrap
- PostgreSQL
- Django
- Heroku
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) 
- [Courier](https://www.courier.com/)
- [Visily](https://www.visily.ai/)
- [IONOS](https://www.ionos.com/)
- [UptimeRobot](https://uptimerobot.com/)

<!-- ## Video Demo
 -->

## Use
Visit www.lulualerts.com! Here, you can browse the home page, login, and sign up pages, available to all visitors without accounts.  Sign up for free to create and manage alerts, as well as to recieve notifications.

9/8/2022: lululemon has removed product data from their HTML, which the app relies on for scraping product attributes, so new alerts cannot be created. The www.lulualerts.com site remains active and functional for all other purposes.  There is a plan to migrate from the current approach (scrape HTML using python beautiful soup library) to a browser simulator (i.e. selenium).  No ETA at the moment.

## Demo
Create and manage alerts:
![create manage alerts](readme/createmanagealert.gif)
<!-- 30fps,large -->

Login & Account creation:
![login](readme/login.gif) ![signup](readme/signup.gif)

<img src="/readme/login.gif" width="50%" height="50%"/>
<img src="/readme/signup.gif" width="50%" height="50%"/>


<!-- ## Challenges, Tradeoffs & future features
- Handling user input
- Making it free - add donations!! uptime robot
- ux
- user notifications improvement! text, more immediate
- managing dev & prod envits w diff settings (static files etc)
 -->

<!-- 
## Testing & monitoring -->

<!-- ## Wading through code -->
