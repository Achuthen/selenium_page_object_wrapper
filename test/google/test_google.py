__author__ = 'achuthen'

import logging
import unittest

from selenium import webdriver

from test.google.google_page import GooglePage


class TextSearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.logger_page_object = logging.getLogger("page_object_logger")
        logging.basicConfig(level=logging.WARN)
        # self.logger_page_object.setLevel(level=logging.DEBUG)
        self.page = GooglePage(self.driver)
        self.page.open()

    def test_text_search(self):
        self.page.search("python")
        self.assertTrue(self.page.search_results_list.get_array_len > 0) # get elements
        # print all the results title, links and summary.
        for index in range(self.page.search_results_list.get_array_len):
            print index
            print self.page.search_results_list[index].title.text.encode('UTF-8')
            print self.page.search_results_list[index].title.get_attribute(
                'href'
            )
            print self.page.search_results_list[index].summary.text

    def test_text_search_first_result(self):
        self.page.search("python") # execute the page object method search
        self.assertEquals(
            self.page.search_results_list[0].title.text,
            "Welcome to Python.org"
        )
        self.assertEquals(
            self.page.search_results_list[0].title.get_attribute(
                'href'
            ),
            "https://www.python.org/"
        )
        self.assertEquals(
            self.page.search_results_list[0].summary.text,
			"The official home of the Python Programming Language."
			)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
