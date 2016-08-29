# -*- coding: utf-8 -*-
from tldextract import extract


# TODO: Need to test for throwing ValueError exception when either domain_url or target_url is None - 2 test cases
class DomainRule:
    @staticmethod
    def apply(domain_url, target_url):
        if domain_url is None or target_url is None:
            raise ValueError("Domain=%s and target URL=%s" % (domain_url, target_url))

        search_domain = extract(domain_url).domain
        url_domain = extract(target_url).domain

        return search_domain == url_domain
