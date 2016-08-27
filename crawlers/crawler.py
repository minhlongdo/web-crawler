# -*- coding: utf-8 -*-
import logging, requests
from queue import LifoQueue
from urllib.parse import urlparse
from parsers.parsers import PageParser
from rules.rules import CrawlSameDomainRule

module_logger = logging.getLogger('WebCrawler')
module_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

fh = logging.FileHandler('web-crawler.log')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

module_logger.addHandler(fh)
module_logger.addHandler(ch)


class Crawler:
    def __init__(self, start_url=None):
        self.start_url = start_url
        
    def crawl(self, start_url=None):
        raise NotImplementedError

    
class WebCrawler(Crawler):
    def __init__(self, start_url=None):
        super().__init__(start_url)
    
    def reconstruct_link(self, link):
        if link is None:
            raise ValueError("Link cannot be None")
        
        url_parsed = urlparse(link)
        
        if url_parsed is None:
            raise ValueError("Something went wrong during the url parsing")
        
        if url_parsed.scheme == 'http' or url_parsed.scheme == 'https':
            module_logger.debug("Uses the http scheme, it is not a relative path.")
            return link
        
        elif url_parsed.scheme == '':
            return self.start_url + url_parsed.path
        
        else:
            raise ValueError("Network location and path are both empty, something is wrong here")
    
    def crawl(self, start_url=None):
        if self.start_url is None and start_url is None:
            raise ValueError("Start url cannot be None")
        
        if start_url is not None:
            self.start_url = start_url
        
        visited = set()
        queue = LifoQueue()
        queue.put(self.start_url)
        
        while not queue.empty():
            tries = 0
            next_link = queue.get()
            
            module_logger.info("Retrieved url=%s from queue" % next_link)
            
            try:
                access_link = self.reconstruct_link(next_link)
                
                if not CrawlSameDomainRule.same_domain(self.start_url, access_link):
                    module_logger.info("url=%s is not in the same domain as %s" % (access_link, self.start_url))
                    continue
                    
                elif access_link in visited:
                    module_logger.info("Already visited url=%s, skipping" % access_link)
                    continue
                
                else:
                    module_logger.info("Going to access url=%s constructed from %s" % (access_link, next_link))
                    
            except ValueError as err:
                module_logger.warn(err)
                continue
            
            if access_link is None:
                raise ValueError("Access link cannot be None,"
                                 "something went wrong in the reconstruct_link access_link=%s" % access_link)
            
            resp = requests.get(access_link)
            
            if resp.status_code != 200:
                module_logger.warn("Unable to access url=%s, response content=%s" % (access_link, resp))
                while tries < 3:
                    tries += 1
                    resp = requests.get(access_link)
                    if resp.status_code == 200:
                        module_logger.info("Able to connect to url=%s after %i retries" % (access_link, tries))
                        break
            
            if resp.status_code != 200:
                module_logger.warn("Failed to access url=%s" % access_link)
                continue
            
            links, assets = PageParser.parse_page_get_links(resp.text)
            
            module_logger.info("Extracted from url=%s - links=%s assets=%s" % (access_link, links, assets))
