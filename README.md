# Web crawler
# Goal
Write a web crawler without using existing crawl frameworks in a programming language of your choice (we prefer Python). Given a URL, the crawler should only visit HTML pages within the same domain and not follow external links (e.g. Facebook, Twitter).
Your crawler should output a site map, and for each page a list of assets (e.g. CSS, Images, Javascripts) and links between pages.
Extra goals
Write it as if it is running in production
Make it run as fast as possible
# Example
Test URL: http://yoyowallet.com/
# Sitemap:
/
/assets.html
/benefits.html
/contact.html
/cookies.html
/founders.html
/index.html
/jobs.html
/legal.html
/retailer.html
/security.html
/support.html
/team.html
... etc
Assets on /index.html:
<a href="*" />, <link rel="*" />, <img src="*" />, <script src="*" />
http://blog.yoyowallet.com
http://www.facebook.com/yoyowallet
http://www.instagram.com/yoyo_wallet
http://www.twitter.com/yoyowallet
http://yoyowallet.com/assets.html
http://yoyowallet.com/founders.html
http://yoyowallet.com/index.html
http://yoyowallet.com/assets/css/bootstrap/bootstr...
http://yoyowallet.com/assets/css/fonts.css
http://yoyowallet.com/assets/css/full-screen.css
http://yoyowallet.com/assets/images/logo.svg
http://yoyowallet.com/assets/js/bootstrap.js
http://yoyowallet.com/assets/js/classie.js
http://yoyowallet.com/assets/js/full-screen.js
... etc

# How to run unittests
Run 'python3 -m unittest discover -p "*_tests.py"' for running all unittests.