# -*- coding: utf-8 -*-
from rules.rules import DomainRule
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

if __name__ == '__main__':
    unittest.main()
