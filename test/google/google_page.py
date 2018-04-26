__author__ = 'achuthen'

from page_object import PageObject, HTMLElement, HTMLElementList


class SearchResults(HTMLElementList):
    title = HTMLElement(xpath='.//h3/a')
    summary = HTMLElement(xpath='.//span[@class="st"]')



class GooglePage(PageObject):
    url = "www.google.com"

    search_box = HTMLElement(name='q')
    google_search_btn = HTMLElement(name='btnG')
    search_results_list = SearchResults(xpath='//div[@id="rso"]//div[@class="g"]')

    def open(self):
        self.logger.info('nav to url: %s' % self.url)
        self.webdriver.get("http://" + self.url)

    def search(self , query):
        #self.google_search_btn.click()
        self.search_box.clear()
        self.search_box.send_keys(query)
        self.search_box.submit()


