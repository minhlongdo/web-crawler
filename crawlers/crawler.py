# -*- coding: utf-8 -*-
import logging, requests
from bs4 import BeautifulSoup
from rules.rules import CrawlSameDomainRule

module_logger = logging.getLogger('WebCrawler')


class Crawler:
    def __init__(self, start_url=None):
        self.start_url = start_url
        
    def crawl(self, start_url=None):
        raise NotImplementedError

    
class WebCrawler(Crawler):
    def __init__(self, start_url=None):
        super().__init__(start_url)
        
    def crawl(self, start_url=None):
        if self.start_url is None and start_url is None:
            raise ValueError("Start url cannot be None")
        
        if start_url is not None:
            self.start_url = start_url