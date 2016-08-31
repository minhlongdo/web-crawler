# -*- coding: utf-8 -*-
from crawlers.crawler import WebCrawler
import pprint

import time

def single_threaded_web_crawler():
	start = time.time()

	try:
		start_url, site_map, links_with_issues = web_crawler.crawl('http://yoyowallet.com/')
	except ValueError as err:
		print(err)

	end = time.time()
	print("Single threaded web crawler total keys: %i" % len(site_map.keys()))
	print("single threaded web crawler total time: %d" % (end - start))

	return site_map

def single_thread_pool_web_crawler():
	start = time.time()

	try:
		start_url, site_map, links_with_issues = web_crawler.start_crawl(workers=1)
	except ValueError as err:
		print(err)

	end = time.time()
	print("Single threaded pool web crawler total keys: %i" % len(site_map.keys()))
	print("Single thread pool worker total time: %d" % (end - start))

	return site_map


def two_threaded_pool_web_crawler():
	start = time.time()

	try:
		start_url, site_map, links_with_issues = web_crawler.start_crawl(workers=2)
	except ValueError as err:
		print(err)

	end = time.time()
	print("Two threaded web crawler total keys: %i" % len(site_map.keys()))
	print("Two thread pool worker total time: %d" % (end - start))

	return site_map

def n_thread_pool_web_Crawler(n):
	start = time.time()

	try:
		start_url, site_map, links_with_issues = web_crawler.start_crawl(workers=n)
	except ValueError as err:
		print(err)

	end = time.time()
	print("%i threaded web crawler total keys: %i" % (n, len(site_map.keys())))
	print("%i thread pool worker total time: %d" % (n, end - start))

	return site_map

def compare_keys(result1, result2):
	if len(result1.keys()) == len(result2.keys()):
		print("Number of keys are the same")
	else:
		print("Different number of keys")

if __name__ == '__main__':
	start_url = 'http://yoyowallet.com/'
	web_crawler = WebCrawler(start_url=start_url)
	pp = pprint.PrettyPrinter(indent=4)

	#single_threaded_result = single_threaded_web_crawler()
	single_thread_pool_result = single_thread_pool_web_crawler()
	#two_threaded_pool_result = two_threaded_pool_web_crawler()
	#ten_threaded_pool_result = n_thread_pool_web_Crawler(10)
	#twenty_threaded_pool_result = n_thread_pool_web_Crawler(20)

	#print(len(single_threaded_result))
	#print(len(single_thread_pool_result))
	#print(len(two_threaded_pool_result))
	#print(len(ten_threaded_pool_result))
	#print(len(twenty_threaded_pool_result))

	#pp.pprint(single_threaded_result)
	pp.pprint(single_thread_pool_result)
	print(len(single_thread_pool_result))
	#pp.pprint(two_threaded_pool_result)
	#pp.pprint(ten_threaded_pool_result)
	#pp.pprint(twenty_threaded_pool_result)

