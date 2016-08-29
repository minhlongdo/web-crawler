# -*- coding: utf-8 -*-
from urllib3.util import parse_url
from tldextract import extract


class CrawlSameDomainRule:
	
	@staticmethod
	def same_domain(domain_url, url):
		search_domain = extract(domain_url).domain
		url_domain = extract(url).domain
		return search_domain == url_domain
