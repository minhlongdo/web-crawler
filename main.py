# -*- coding: utf-8 -*-
from crawlers.crawler import WebCrawler


if __name__ == '__main__':
	start_url = 'http://yoyowallet.com/'
	web_crawler = WebCrawler(start_url=start_url)
	try:
		web_crawler.crawl()
		
	except ValueError as err:
		print(err)
