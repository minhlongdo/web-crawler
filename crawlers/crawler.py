# -*- coding: utf-8 -*-
import logging
from queue import LifoQueue
from parsers.parsers import PageParser
from rules.rules import DomainRule, FileExtensionRule
from handlers.http_handler import HttpHandler
from handlers.link_handler import LinkHandler

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

    
class WebCrawler:
    def __init__(self, start_url=None):
        self.start_url = start_url
    
    def crawl(self, start_url=None):
        if self.start_url is None and start_url is None:
            raise ValueError("Start url cannot be None")
        
        if start_url is not None:
            self.start_url = start_url
        
        site_map = dict()
        visited = set()
        links_with_issues = set()
        queue = LifoQueue()
        queue.put(self.start_url)
        
        print("Crawling start")
        
        while not queue.empty():
            print("Current queue size=%i" % queue.qsize())
            next_link = queue.get()
            
            module_logger.info("Retrieved url=%s from queue" % next_link)

            try:
                if FileExtensionRule.apply(next_link):
                    module_logger.info("Url=%s is a file asset" % next_link)
                    continue

            except ValueError as err:
                module_logger.warn(err)

            try:
                access_link = LinkHandler.reconstruct_link(self.start_url, next_link)

                if access_link is None:
                    module_logger.warn("Currently working on next_link=%s - But access link value is None,"
                                       "Something went wrong during the link construction" % next_link)
                    links_with_issues.add(next_link)
                    continue

                elif access_link in visited:
                    module_logger.info("Already visited url=%s, skipping" % access_link)
                    continue

                elif not DomainRule.apply(self.start_url, access_link):
                    module_logger.info("url=%s is not in the same domain as %s" % (access_link, self.start_url))
                    continue

                else:
                    module_logger.info("Going to access url=%s constructed from %s" % (access_link, next_link))
                    
            except ValueError as err:
                module_logger.warn(err)
                links_with_issues.add(next_link)
                continue
            
            except Exception as err:
                module_logger.error("An unexpected error during the link construction of url=%s" % next_link, err)
                links_with_issues.add(next_link)
                continue
            
            try:
                content = HttpHandler.fetch_url_content(access_link)

                if content is None:
                    module_logger.warn("Unable to get content from link=%s" % access_link)
                    continue
            
            except ValueError as err:
                module_logger.warn("Link=%s has a value issue, value current is %s" % (access_link, content), err)
                module_logger.exception(err)
                continue
            
            except Exception as err:
                module_logger.warn("Something unexpected happened while fetching content of the url=%s"
                                   % access_link)
                module_logger.exception(err)
                continue
            
            links, assets = PageParser.parse_page_get_links(content)
            
            module_logger.debug("Add link=%s into already visited list" % next_link)
            
            visited.add(next_link)
            
            module_logger.info("Extracted from url=%s - links=%s assets=%s" % (access_link, links, assets))
            
            for link in links:
                if link not in visited:
                    queue.put(link)
                
            module_logger.debug("Current link queue=%s" % str(queue))
            site_map_record = {next_link: {'links': links, 'assets': assets}}
            
            module_logger.info("Adding record into site map=%s" % site_map_record)
            
            site_map.update(site_map_record)
        
        module_logger.info("Crawling completed.")
        print("Crawling completed")
        
        module_logger.info("SiteMap=%s" % site_map)
        module_logger.info("Links with issues=%s" % links_with_issues)
        
        return self.start_url, site_map, links_with_issues
