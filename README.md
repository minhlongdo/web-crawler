# Web crawler
# Goal
Write a web crawler without using existing crawl frameworks in a programming language of your choice (we prefer Python). Given a URL, the crawler should only visit HTML pages within the same domain and not follow external links (e.g. Facebook, Twitter).
Your crawler should output a site map, and for each page a list of assets (e.g. CSS, Images, Javascripts) and links between pages.
Extra goals
Write it as if it is running in production
Make it run as fast as possible
# How to run unittests
Run 'python3 -m unittest discover -p "*_tests.py"' for running all unittests.