__author__ = 'achuthen'
import logging
from abc import ABCMeta, abstractmethod
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException , WebDriverException
# modified from page object python library.

# Map PageElement constructor arguments to webdriver locator enums
_LOCATOR_MAP = {'css': By.CSS_SELECTOR,
                'id_': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'link_text': By.LINK_TEXT,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
                'tag_name': By.TAG_NAME,
                'class_name': By.CLASS_NAME,
                }

# Map PageElement constructor arguments to webdriver locator enums
_EXPECTED_COND_ELEMENT = {'presence': expected_conditions.presence_of_element_located,
                  'visible': expected_conditions.visibility_of_element_located,
                  'frame_available': expected_conditions.frame_to_be_available_and_switch_to_it,
                  'invisible': expected_conditions.invisibility_of_element_located,
                  'nopresence': expected_conditions.invisibility_of_element_located,
                  'clickable': expected_conditions.element_to_be_clickable,
                  'selected': expected_conditions.element_to_be_clickable
}

_EXPECTED_COND_ELEMENTS = {'presence': expected_conditions.presence_of_all_elements_located,
                  'visible': expected_conditions.visibility_of_any_elements_located,
}


class PageObject(object):
    """Page Object pattern."""
    __metaclass__ = ABCMeta
	
    def __init__(self, webdriver):
        """
        :param webdriver: selenium webdriver instance.
        :return: returns the page object
        """
        self.webdriver = webdriver
        self.logger = logging.getLogger("page_object_logger")

    @property
    def title(self):
        return self.webdriver.title

class Element(object):
    """Element descriptor."""
    __metaclass__ = ABCMeta
	
    TIMEOUT = 10
    _expected_condition = 'visible' # default value
    _expected_cond_map = _EXPECTED_COND_ELEMENT
    _locator = None
    _wait_timeout = TIMEOUT
    _find_retries = 3
	
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("page_object_logger")
        if not kwargs:
            raise ValueError("Please specify a locator")
        len_kwargs = len(kwargs)
        if len_kwargs > 2:
            raise ValueError("Element only takes 2 arguments , but %d given" % len_kwargs)
        for key, value in kwargs.iteritems():
            if key in _LOCATOR_MAP:
                self._locator = (_LOCATOR_MAP[key], value)
            elif key == "expected_condition":
                self._expected_condition = value
                if value not in self._expected_cond_map:
                    raise ValueError("INVALID expected condition %s", value)
            elif key == "wait_timeout":
                if isinstance(value, int) and value > 0:
                    self._wait_timeout = value
                else:
                    raise ValueError("invalid wait_timeout")
            else:
                raise ValueError("INVALID input: %s", key)
        if self._locator is None:
            raise ValueError("Please specify a locator")


    def find(self):
        self.logger.debug('Find %s by %s: <%s>', self.__class__.__name__, *self._locator)
        tries = 3
        while True:
            try:
                return WebDriverWait(self.parent_ele, self._wait_timeout).until(
                    self._expected_cond_map[self._expected_condition](self._locator),
                    "Didn't find element by %s: <%s>" % self._locator)
            except StaleElementReferenceException as e:
                self.logger.debug("StaleElementReferenceException found on parent. Retry find parent: %s"
                                 % self.parent_pageelement.__class__.__name__)
                self.parent_ele = self.parent_pageelement._refind_element()
                time.sleep(1)
                tries -= 1
                if tries == 0:
                    self.logger.error("failed to find the element after %d retries" % tries)
                    raise e

    def __get__(self, instance, owner):
        if isinstance(instance, PageObject):
            self.logger.debug("Finding %s under %s ", self.__class__.__name__, instance.__class__.__name__)
            self.parent_ele = instance.webdriver
        elif isinstance(instance, Element):
            self.logger.debug("Finding child element of %s",  instance.__class__.__name__)
            # print instance.element.get_attribute('class')
            self.parent_ele = instance.element
        else:
            raise ValueError("PageElement of ParentPageElement can only be instantiated on PageObject or ParentPageElement ")
        self.parent_pageelement = instance
        self.element = self.find()
        return self

    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            value = str(value)
            if len(value) > 0:
                self.logger.debug("Type text '%s' into the element")
                self.element.send_keys(value)
                return 1


    def _refind_element(self):
        self.logger.debug("Refind element")
        return self.find()

    @property
    def native_webelement(self):
        # if self._expected_cond_map == _EXPECTED_COND_ELEMENT:
        #     return self.element
        # else:
        #     raise ("get_array_len can only be called on PageElement or ParentElement objects")
        return self.element

    def __click(self):
        return self.element.click()

    def __send_keys(self, value):
        return self.element.send_keys(value)


    def __swtich_case_for_webelement_actions(self, actions_str, value=None):
        switcher = {
            'click': self.__click(),
            'send_keys:': self.__send_keys(value)
        }
        return switcher.get(actions_str, "None")

    def _wrapper_webelement_actions(self, action, value=None):
        tries = 3
        while True:
            try:
                if action == "click":
                    ret = self.element.click()
                elif action == "send_keys":
                    ret = self.element.send_keys(value)
                elif action == "clear":
                    ret = self.element.clear()
                elif action == "text":
                    ret = self.element.text
                elif action == "get_attribute":
                    ret = self.element.get_attribute(value)
                elif action == "is_displayed":
                    ret = self.element.is_displayed()
                elif action == "submit":
                    ret = self.element.submit()
                elif action == "is_enabled":
                    ret = self.element.is_enabled()
                elif action == "is_selected":
                    ret = self.element.is_selected()
                else:
                    raise "Action Not defined. Library Script Issue"

            except (StaleElementReferenceException, WebDriverException) as e:
                self.logger.debug("retrying... ")
                time.sleep(1)
                self.element = self._refind_element()
                # if self._expected_cond_map == _EXPECTED_COND_ELEMENT:
                #     self.element = self.()
                # elif self._expected_cond_map == _EXPECTED_COND_ELEMENTS:
                #     #todo: check for index rather than this. define index at the begining to none.
                #     self.element = self.find()[self.index_item]
                # else:
                #     raise ("get_array_len can only be called on PageElement or ParentElement objects")

                # todo parent researching.
                tries -= 1
                if tries == 0:
                    self.logger.error("after 3 retries to click still failed to click")
                    raise e
            else:
                return ret

    def click(self):
        return self._wrapper_webelement_actions('click')

    def clear(self):
        return self._wrapper_webelement_actions('clear')

    def send_keys(self, value):
        return self._wrapper_webelement_actions('send_keys', value)

    @property
    def text(self):
        return self._wrapper_webelement_actions('text')

    def get_attribute(self, value):
        return self._wrapper_webelement_actions('get_attribute', value)

    def is_displayed(self):
        return self._wrapper_webelement_actions('is_displayed')

    def submit(self):
        return self._wrapper_webelement_actions('submit')

    def is_enabled(self):
        return self._wrapper_webelement_actions('is_enabled')

    def is_selected(self):
        return self._wrapper_webelement_actions('is_selected')

    def parent(self):
        return self.parent


class ListElements(Element):

    _expected_cond_map = _EXPECTED_COND_ELEMENTS

    def __get__(self, instance, owner):
        super(ListElements, self).__get__(instance, owner)
        self.elements = self.element
        return self

    def __getitem__(self, item):
        # dict_element = {}
        # for index, ele in enumerate(self.element):
        #     dict_element[index] = ele
        self.index_item = item
        # since this is list elements, need to replace the self.element to the item we need.
        self.element = self.element[item]
        #self.parent_pageelement = self[item]
        return self


    def _refind_element(self):
        self.logger.debug("Refind element with index %s" % self.index_item)
        return self.find()[self.index_item]

    # access only by parent class or guardedelements
    @property
    def get_array_len(self):
        # indicates the array of elements
        if self._expected_cond_map == _EXPECTED_COND_ELEMENTS:
            return len(self.element)
        else:
            raise ("get_array_len can only be called on a element list object, PageElements or ParentElements")

    @property
    def native_webelements(self):
        return self.elements

		
class HTMLElement(Element):
	pass
	
	
class HTMLElementList(ListElements):
	pass
