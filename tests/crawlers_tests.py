# -*- coding: utf-8 -*-
from crawlers.crawler import WebCrawler
import unittest


class WebCrawlerTest(unittest.TestCase):
	def test_webcrawler_crawl_value_error(self):
		webcrawler = WebCrawler()
		self.assertRaises(ValueError, webcrawler.crawl)

if __name__ == '__main__':
	unittest.main()