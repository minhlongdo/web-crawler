# -*- coding utf-8 -*-
from urllib.parse import urlparse

import logging

module_logger = logging.getLogger('LinkHandler')
module_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

fh = logging.FileHandler('link-handler.log')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

module_logger.addHandler(fh)
module_logger.addHandler(ch)


class LinkHandler:

    @staticmethod
    def reconstruct_link(start_url, link):
        """
        Determines with the given link is a relative or absolute link.
        If it is a relative link, e.g. assets/pic.png and the domain is http://yoyowallet.com/
        then it will attempt to reconstruct an absolute link.

        The expected absolute link will be http://yoyowallet.com/assets/pic.png

        If the input link is an absolute link, it will be returned as it is.

        :param start_url: link that the absolute link is referring to
        :param link: possible relative like, might also be an absolute link
        :return: link (str) | ValueError
        """
        if link is None:
            raise ValueError("Link cannot be None")

        url_parsed = urlparse(link)

        if url_parsed is None:
            raise ValueError("Something went wrong during the url parsing")

        if url_parsed.scheme == 'http' or url_parsed.scheme == 'https':
            module_logger.debug("Uses the http scheme, it is not a relative path.")
            return link

        elif url_parsed.scheme == '':
            start_url_parsed = urlparse(start_url)

            if start_url_parsed is None or start_url_parsed.path == '':
                absolute_link = start_url_parsed.scheme + "://" + start_url_parsed.netloc + '/' + url_parsed.path
                module_logger.info("absolute_link=%s" % absolute_link)

                return absolute_link

            else:
                absolute_link = start_url + url_parsed.path
                module_logger.info("absolute_link=%s" % absolute_link)

                return absolute_link

        else:
            raise ValueError("Network location and path are both empty, something is wrong here")