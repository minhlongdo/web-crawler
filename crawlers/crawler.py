# -*- coding: utf-8 -*-
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    def start_crawl(self, workers=1):
        """
        Start webcrawler workers using threads.
        Url are submitted to a threadpoolexecutor, results are being actively polled.
        Returned results are saved in 'site_map' while putting new links that were found in the url into the queue.
        :param num_thread: Number of workers to run
        :return: self.start_url - set(), site_map - dict(), links_with_issues - set()
        """
        site_map = {}
        visited = set()
        links_with_issues = set()
        queue = set()

        if not self.start_url:
            raise ValueError("Invalid starting url value, starting_url=%s" % self.start_url)

        if workers < 1:
            raise ValueError("The number of workers need to be at least 1.")

        queue.add(self.start_url)
        jobs = 0

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_url = dict()
            while len(queue) > 0 or jobs > 0:
                while len(queue) > 0:
                    url = queue.pop()
                    future_to_url[executor.submit(self.crawl_worker, url)] = url
                    jobs += 1

                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    visited.add(url)

                    jobs -= 1

                    if future.exception() is not None:
                        module_logger.warn('%r generated an exception: %s' % (url,
                                                                              future.exception()))
                    else:
                        site_map_entry, links_with_issues_entry = future.result()
                        module_logger.info("Visited=%s linksWithIssues=%s Sitemap=%s" % (visited, links_with_issues, site_map))

                        if site_map_entry is not None:
                            site_map.update(site_map_entry)

                            try:
                                links = site_map_entry[url]['links']

                                # Add links that were retrieved from the url to the queue
                                # Conditions: must not be 'None' or in visited or valid based on the FileExtensionRule
                                next_url_batch = [link for link in links
                                                  if link is not None
                                                  and link not in visited
                                                  and not FileExtensionRule.apply(link)]

                                for next_url in next_url_batch:
                                    queue.add(next_url)

                            except ValueError as err:
                                module_logger.warn(err)

                            except KeyError as err:
                                module_logger.warn(err)

                            except Exception as err:
                                module_logger.warn(err)

                        # Record links that had issues
                        if links_with_issues_entry is not None:
                            for link in links_with_issues_entry:
                                links_with_issues.add(link)

                # Resizing future dictionary - cleaning up after the result has been processed
                future_to_url = { k:v for k,v in future_to_url.items() if v not in visited }

        return site_map, links_with_issues

    def crawl_worker(self, url):
        """
        This is the task that is being executed by the threadpool executor when it receive a url to do it's job
        :param url: Url that is supposed to be getting links and assets from
        :return: site_map_entry - dict(), links_with_issues_entry - set()
        """
        if url is None:
            raise ValueError("Url=%s has a None value" % url)

        site_map_entry = dict()
        links_with_issues_entry = set()

        module_logger.info("Working on url=%s" % url)

        try:
            # Make a relative url into an absolute url
            access_link = LinkHandler.reconstruct_link(self.start_url, url)

            if access_link is None:
                raise ValueError("Access link value: %s" % access_link)

            elif not DomainRule.apply(self.start_url, access_link):
                module_logger.info("url=%s is not in the same domain as %s" % (access_link, self.start_url))
                module_logger.debug("Start url=%s site_map_entry=%s links_with_issues_entry=%s" % (self.start_url,
                                                                                                   site_map_entry,
                                                                                                   links_with_issues_entry))
                return None, links_with_issues_entry

            module_logger.debug("Going to open access_link=%s" % access_link)

        except Exception as err:
            module_logger.warn(err)
            site_map_entry[url] = {'links': set(), 'assets': set()}
            return None, links_with_issues_entry


        try:
            content = HttpHandler.fetch_url_content(access_link)

            if content is None:
                raise ValueError("Content of the url=%s is None" % url)

        except ValueError as err:
            module_logger.warn(err)
            return None, links_with_issues_entry

        except Exception as err:
            module_logger.warn(err)
            return None, links_with_issues_entry

        links, assets = PageParser.parse_page_get_links(content)

        site_map_entry[url] = {'links': links, 'assets': assets}

        module_logger.info("Completed working on url=%s" % url)

        module_logger.info("SiteMap=%s" % site_map_entry)
        module_logger.info("Links with issues=%s" % links)

        return site_map_entry, links_with_issues_entry


    def crawl(self, start_url=None):
        """
        Single threaded webcrawler.
        :param start_url: Starting url
        :return: starting url (str), sitemap (dict), links with issues (set)
        """
        if self.start_url is None and start_url is None:
            raise ValueError("Start url cannot be None")

        if start_url is not None:
            self.start_url = start_url

        site_map = dict()
        visited = set()
        links_with_issues = set()
        queue = LifoQueue()
        queue.put(self.start_url)

        while not queue.empty():
            next_link = queue.get()

            module_logger.info("Retrieved url=%s from queue" % next_link)

            try:
                if FileExtensionRule.apply(next_link):
                    module_logger.info("Url=%s is a file asset" % next_link)
                    continue

            except ValueError as err:
                module_logger.warn(err)

            try:
                # Create an absolute url from a relative url
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

            # Get links and assets from HTML page
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

        module_logger.info("SiteMap=%s" % site_map)
        module_logger.info("Links with issues=%s" % links_with_issues)

        return self.start_url, site_map, links_with_issues
