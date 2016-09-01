# -*- coding: utf-8 -*-
from tldextract import extract
from urllib.parse import urlparse

from os.path import splitext
from logging.handlers import RotatingFileHandler
import logging

module_logger = logging.getLogger('Rules')
module_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

fh = RotatingFileHandler('rules.log', maxBytes=100000, backupCount=5)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

module_logger.addHandler(fh)
module_logger.addHandler(ch)


class DomainRule:
    @staticmethod
    def apply(domain_url, target_url):
        """
        Check if the url belongs to the same domain.

        :param domain_url: Domain that the url is supposed to be validated against.
        :param target_url: Url that needs to be validated against the domain url.
        :return: True | False
        """
        if domain_url is None or target_url is None:
            raise ValueError("Domain=%s and target URL=%s" % (domain_url, target_url))

        search_domain = extract(domain_url).domain
        url_domain = extract(target_url).domain

        return search_domain == url_domain


class FileExtensionRule:
    @staticmethod
    def apply(url):
        """
        Only return True for .html extensions as they are possible links.
        Everything else such as .zip will return False

        :param url: source link for asset
        :return: True | False
        """
        if url is None:
            raise ValueError("Url=%s" % url)

        parsed_url = urlparse(url)

        if parsed_url is None:
            raise ValueError("Parsed url=%s" % parsed_url)

        scheme = parsed_url.scheme

        # Condition for a relative path to be an asset - E.g. compressed file
        if scheme is None or scheme == '':
            filename, file_ext = splitext(url)
            if file_ext is None or file_ext == '' or file_ext == '.html':
                module_logger.debug("Url=%s is not a file asset" % url)
                return False

            else:
                module_logger.debug("Url=%s is a file asset" % url)
                return True
        else:
            module_logger.debug("Scheme=%s Url=%s is not a file asset" % (scheme, url))
            return False
