# -*- coding: utf-8 -*-
from urllib3.util import parse_url


class CrawlSameDomainRule:
	
	@staticmethod
	def same_domain(domain_url, url):
		search_domain = parse_url(domain_url).hostname
		return search_domain in url
