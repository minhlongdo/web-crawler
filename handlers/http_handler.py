# -*- coding utf-8 -*-
import logging
import requests

module_logger = logging.getLogger('HttpHandler')
module_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

fh = logging.FileHandler('http-handler.log')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

module_logger.addHandler(fh)
module_logger.addHandler(ch)


class HttpHandler:

    @staticmethod
    def fetch_url_content(url):
        """
        Fetches content from url through a GET request.

        :param url: A valid url
        :return: content
        """
        if url is None or url == '':
            raise ValueError("Url=%s" % url)

        try:
            resp = requests.get(url)

            if resp.status_code != 200:
                module_logger.warn("Unable to access url=%s, response=%s" % (url, resp))

            if resp is None:
                module_logger.warn("response content=%s for url=%s" % (resp, url))
                raise ValueError("response content=%s for url=%s" % (resp, url))

            return resp.text

        except ConnectionError as err:
            module_logger.warn(err)
            raise ConnectionError(err)

        except Exception as err:
            module_logger.warn(err)
            raise Exception(err)