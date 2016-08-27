# -*- coding: utf-8 -*-
from crawlers.crawler import WebCrawler
import pprint


if __name__ == '__main__':
	start_url = 'http://yoyowallet.com/'
	web_crawler = WebCrawler(start_url=start_url)
	pp = pprint.PrettyPrinter(indent=4)
	
	try:
		start_url, site_map, links_with_issues = web_crawler.crawl()
		
		pp.pprint(start_url)
		pp.pprint(site_map)
		pp.pprint(links_with_issues)
		
	except ValueError as err:
		print(err)
