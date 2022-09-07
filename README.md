# lulu alerts
<!-- ![lulualerts logo](retail_alerts/lulu_alerts/static/lulu_alerts/big_icon.png) -->
![homepage gif](readme/homepageloop.gif)

## Project overview
lulu alerts makes sure shoppers don't miss out on purchasing their favorite lululemon products as soon as they go on sale or come back in stock with notifications delivered to their inboxes 

### Description
lulu alerts is a web application for creating and managing alerts for lululemon products.  Users create lulu alerts accounts, then they can configure two different types of alerts: (1) "back in stock" alerts, which tell a user when a particular out of stock product shows back up on in stock on lululemon.com, as well as (2) "price drop" alerts, which tell a user when a particular product has fallen in price.  lulu alerts uses web scraping to grab product attributes.  On an ongoing basis, the app checks lululemon.com to see if any of its user's configured alerts should be triggered by a particular product price change or product back in stock, and notifies them via email.

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
