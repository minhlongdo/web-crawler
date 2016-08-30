# -*- coding utf-8 -*-
from handlers.link_handler import LinkHandler
from hamcrest import assert_that, is_

import unittest


class LinkHandlerTest(unittest.TestCase):
    def test_reconstruct_link_no_action_needed(self):
        start_url = 'start_link'
        url = 'http://google.com'

        link = LinkHandler.reconstruct_link(start_url, url)

        assert_that(link, is_(url))

    def test_reconstruct_link(self):
        start_url = "https://yoyowallet.com/"
        url = 'assets'

        expected_link = start_url + url

        link = LinkHandler.reconstruct_link(start_url, url)

        assert_that(link, is_(expected_link))

    def test_reconstruct_link_without_domain_forwardslash(self):
        start_link = "https://yoyowallet.com"
        url = "assets"

        expected_link = "https://yoyowallet.com/assets"

        link = LinkHandler.reconstruct_link(start_link, url)

        assert_that(link, is_(expected_link))

if __name__ == '__main__':
    unittest.main()