# -*- coding: utf-8 -*-
from rules.rules import CrawlSameDomainRule
from hamcrest import assert_that, is_

import unittest


class CrawlSameDomainRuleTest(unittest.TestCase):
    def test_same_domain_expect_pass(self):
        domain = "http://yoyowallet.com/"
        url = "http://blog.yoyowallet.com/"

        result = CrawlSameDomainRule.same_domain(domain, url)

        assert_that(result, is_(True))

    def test_same_domain_expect_fail(self):
        domain = "http://yoyowallet.com/"
        url = "http://google.com/"

        result = CrawlSameDomainRule.same_domain(domain, url)

        assert_that(result, is_(False))

    def test_same_domain_with_google_expect_fail(self):
        domain = "http://yoyowallet.com/"
        url = "https://accounts.google.com/SignUpWithoutGmail?dsh=5061114340578854825&continue=https%3A%2F%2Fplus.google.com%2Fshare%3Furl%3Dhttp%3A%2F%2Fblog.yoyowallet.com%2Facquisition-news%2F%26gpsrc%3Dgplp0&service=oz"

        result = CrawlSameDomainRule.same_domain(domain, url)

        assert_that(result, is_(False))


if __name__ == '__main__':
    unittest.main()
