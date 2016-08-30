# -*- coding: utf-8 -*-
from rules.rules import DomainRule, FileExtensionRule
from hamcrest import assert_that, is_

import unittest


class DomainRuleTest(unittest.TestCase):
    def test_same_domain_expect_pass(self):
        assert_that(DomainRule.apply(domain_url="http://yoyowallet.com/",
                                     target_url="http://blog.yoyowallet.com/"),
                    is_(True))

    def test_same_domain_expect_fail(self):
        assert_that(DomainRule.apply(domain_url="http://yoyowallet.com/",
                                      target_url="http://google.com"),
                    is_(False))

    def test_same_domain_with_google_accounts(self):
        assert_that(DomainRule.apply(domain_url="http://yoyowallet.com/",
                                     target_url="https://accounts.google.com/SignUpWithoutGmail?dsh=5061114340578854825&continue=https%3A%2F%2Fplus.google.com%2Fshare%3Furl%3Dhttp%3A%2F%2Fblog.yoyowallet.com%2Facquisition-news%2F%26gpsrc%3Dgplp0&service=oz"),
                    is_(False))


class FileExtensionRuleTest(unittest.TestCase):
    def test_file_extension_expect_pass(self):
        url = 'downloads/founders.zip'
        assert_that(FileExtensionRule.apply(url), is_(True))

    def test_file_extension_website_html_expect_fail(self):
        url = 'legal.html'
        assert_that(FileExtensionRule.apply(url), is_(False))

    def test_file_extension_hyperlink_http_expect_pass(self):
        url = 'http://google.com'
        assert_that(FileExtensionRule.apply(url), is_(False))

    def test_file_extension_hyperlink_https_expect_pass(self):
        url = 'https://google.com'
        assert_that(FileExtensionRule.apply(url), is_(False))


if __name__ == '__main__':
    unittest.main()
