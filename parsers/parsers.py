# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class PageParser:
	@staticmethod
	def parse_page_get_links(html_doc):
		if html_doc is None:
			raise ValueError("html is not specified")
		
		soup = BeautifulSoup(html_doc, 'html.parser')
		links = set()
		assets = set()
		
		for link in soup.find_all({'a', 'link', 'img', 'script', 'source'}):
			if link.name == 'a':
				links.add(link.get('href'))
			else:
				url = link.get('src') or link.get('href')
				assets.add(url)
		
		return links, assets
