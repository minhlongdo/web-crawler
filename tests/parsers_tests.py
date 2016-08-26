# -*- coding: utf-8 -*-
from parsers.parsers import PageParser
import unittest


class PageParserTest(unittest.TestCase):
	def test_get_links(self):
		html_doc = """
		<html><head><title>The Dormouse's story</title></head>
		<body>
		
		<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
		<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
		<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
		<source src="assets/vids/bg-video.mp4" type="video/mp4">,
		<img src="assets/images/screenshots/rewards.png" alt="" class="overlay-icon">,
		<script async="" src="https://www.google-analytics.com/analytics.js"></script>
		"""
		
		page_parser = PageParser()
		links, assets = page_parser.parse_page_get_links(html_doc)
		
		expected_links = ["http://example.com/elsie", "http://example.com/lacie", "http://example.com/tillie"]
		
		expected_assets = ["assets/vids/bg-video.mp4", "assets/images/screenshots/rewards.png",
		                   "https://www.google-analytics.com/analytics.js"]
		
		self.assertIsNotNone(links)
		self.assertIsNotNone(assets)
		self.assertEquals(len(links), len(expected_links))
		self.assertEquals(len(assets), len(expected_assets))
		self.assertEqual(set(links) == set(expected_links), True)
		self.assertEqual(set(assets) == set(expected_assets), True)
		
if __name__ == '__main__':
	unittest.main()
