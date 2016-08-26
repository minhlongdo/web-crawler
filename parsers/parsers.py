# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class PageParser:
	@staticmethod
	def parse_page_get_links(html_doc):
		if html_doc is None:
			raise ValueError("html is not specified")
		
		soup = BeautifulSoup(html_doc, 'html.parser')
		return set(link.get('href') or link.get('src') or link.get('rel') for link in soup.find_all({'a', 'link', 'img', 'script', 'source'})
		           if link.get('href') is not None or link.get('src') is not None or link.get('rel'))
	
	@staticmethod
	def parse_page_get_assets(html_doc):
		if html_doc is None:
			raise ValueError("html is not specified")
		
		soup = BeautifulSoup(html_doc, 'html.parser')
		return set(asset.get('href') or asset.get('src') for asset in soup.find_all({'a', 'link', 'img', 'script'})
		           if asset.get('href') is not None or asset.get('src') is not None)
