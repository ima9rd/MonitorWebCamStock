import requests
from bs4 import BeautifulSoup as bs
from collections.abc import Iterable
import time

class BaseSearch:
    def __init__(self):
        self.vendor_name = None
        self.javascript = False
        self.loaded_element = None
        self.driver = None
        self.stock_labels = None
        self.watched_skus = None
        self.require_user_agent = False
        self.headers = {'user-agent': 'fake-app/1.0.0'}
        self.base_url = None
        self.search_url = None
        self.items = None
        self.found = []
        self.sku_found = 0
        self.search_hierarchy = []
        self.initialize()
        if self.require_user_agent == True:
            from fake_useragent import UserAgent
            self.user_agent = UserAgent()
        if self.javascript:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.headless = True
            options.add_argument('user-agent={0}'.format(self.headers['user-agent']))
            self.driver = webdriver.Chrome(chrome_options=options)
        self.start_search()

    def initialize(self):
        return

    def search_step(self, step, item):
        if step['multi']:
            return item.find_all(step['tag'], step['search'])
        else:
            return item.find(step['tag'], step['search'])

    def process_items(self):
        return

    def print_results(self):
        if len(self.found) > 0:
            print(self.found)
        elif self.sku_found > 0:
            print('{}: no items in stock.'.format(self.vendor_name))
        else:
            print('{}: failed to find results.'.format(self.vendor_name))

    def start_search(self):
        if self.require_user_agent:
            self.headers['user-agent'] =  self.user_agent.random
        if self.javascript:
            self.driver.implicitly_wait(10)
            self.driver.get(self.search_url)
            if self.loaded_element:
                self.driver.find_element_by_id(self.loaded_element)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            html = self.driver.page_source
            self.driver.quit()
            self.items = bs(html, 'html.parser')
        else: 
            self.items = bs(requests.get(self.search_url, headers=self.headers).text, 'html.parser')
        for step in self.search_hierarchy:
            if isinstance(self.items, list):
                temp = list()
                for item in self.items:
                    if isinstance(item, list):
                        for i in item:
                            temp.append(self.search_step(step, i))
                    else:
                        temp.append(self.search_step(step, item))
                if len(temp) > 0:
                    self.items = temp
            else:
                self.items = self.search_step(step, self.items)
        self.process_items()

