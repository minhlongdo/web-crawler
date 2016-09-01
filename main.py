# -*- coding: utf-8 -*-
from crawlers.crawler import WebCrawler
import pprint

import time

def single_threaded_web_crawler():
	start = time.time()

	try:
		start_url, site_map, links_with_issues = web_crawler.crawl('http://yoyowallet.com/')
		end = time.time()
		print("Single threaded web crawler total keys: %i" % len(site_map.keys()))
		print("single threaded web crawler total time: %d" % (end - start))

		return site_map
	except ValueError as err:
		print(err)

	except Exception as err:
		print(err)

def single_thread_pool_web_crawler():
	start = time.time()

	try:
		site_map, links_with_issues = web_crawler.start_crawl(workers=1)
		end = time.time()
		print("Single threaded pool web crawler total keys: %i" % len(site_map.keys()))
		print("Single thread pool worker total time: %d" % (end - start))

		return site_map

	except ValueError as err:
		print(err)
	except Exception as err:
		print(err)

def two_threaded_pool_web_crawler():
	start = time.time()

	try:
		site_map, links_with_issues = web_crawler.start_crawl(workers=2)
		print("Two threaded web crawler total keys: %i" % len(site_map.keys()))
		end = time.time()
		print("Two thread pool worker total time: %d" % (end - start))
		return site_map
	except ValueError as err:
		print(err)
	except Exception as err:
		print(err)

def n_thread_pool_web_Crawler(n):
	start = time.time()

	try:
		site_map, links_with_issues = web_crawler.start_crawl(workers=n)
		end = time.time()
		print("%i threaded web crawler total keys: %i" % (n, len(site_map.keys())))
		print("%i thread pool worker total time: %d" % (n, end - start))
		return site_map

	except ValueError as err:
		print(err)
	except Exception as err:
		print(err)

def compare_keys(result1, result2):
	if len(result1.keys()) == len(result2.keys()):
		print("Number of keys are the same")
	else:
		print("Different number of keys")

	result1_set = set()
	for key in result1.keys():
		result1_set.add(key)

	result2_set = set()
	for key in result2.keys():
		result2_set.add(key)

	diff1 = result1_set.difference(result2_set)
	print("Number of differences=%i" % len(diff1))
	print("Differences: %s" % diff1)

	diff2 = result2_set.difference(result1_set)
	print("Number of differences=%i" % len(diff2))
	print("Differences: %s" % diff2)

if __name__ == '__main__':
	start_url = 'http://yoyowallet.com/'
	web_crawler = WebCrawler(start_url=start_url)
	pp = pprint.PrettyPrinter(indent=4)

	#single_threaded_result = single_threaded_web_crawler()
	#single_thread_pool_result = single_thread_pool_web_crawler()
	two_threaded_pool_result = two_threaded_pool_web_crawler()
	ten_threaded_pool_result = n_thread_pool_web_Crawler(10)
	#twenty_threaded_pool_result = n_thread_pool_web_Crawler(20)

	#print(len(single_threaded_result))
	#print(len(single_thread_pool_result))
	print(len(two_threaded_pool_result))
	print(len(ten_threaded_pool_result))
	#print(len(twenty_threaded_pool_result))

	#pp.pprint(single_threaded_result)
	#print(len(single_threaded_result))
	##pp.pprint(single_thread_pool_result)
	#print(len(single_thread_pool_result))
	#pp.pprint(two_threaded_pool_result)
	#pp.pprint(ten_threaded_pool_result)
	#pp.pprint(twenty_threaded_pool_result)

	#compare_keys(single_threaded_result, single_thread_pool_result)
