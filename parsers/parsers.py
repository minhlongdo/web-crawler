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

		# Get links and assets
		for link in soup.find_all({'a', 'link', 'img', 'script', 'source'}):
			if link.name == 'a':
				link = link.get('href')
				if link is not None:
					links.add(link)
			else:
				url = link.get('src') or link.get('href')
				if url is not None:
					assets.add(url)

		return links, assets
