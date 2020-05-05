from base_search_class import BaseSearch
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs


class TargetSearch(BaseSearch):

    def initialize(self):
        self.vendor_name = 'Target'
        self.javascript = True
        self.stock_labels = ['Sold out', 'Shipping temporarily out of stock', 'Shipping not available', 'Shipping temporarily out of stock ']
        self.watched_skus = ['A-13252212', 'A-76168087', 'A-79154883', 'A-79154850', 'A-79154748']
        self.base_url ='https://www.target.com'
        self.search_url = 'https://www.target.com/s?searchTerm=webcam&facetedValue=fwtfr'
        self.requires_user_agent = True
        self.loaded_element = 'master-1'
        self.search_hierarchy = [
            {'multi': True, 'tag': 'div', 'search': {'data-test': 'product-details'}}
        ]

    def process_items(self):
        for item in self.items:
            if not item:
                pass
            else:
                item_url = item.find('a', {'data-test': 'product-title'})
                if item_url:
                    item_url = item_url['href']
                    sku = item_url.split('/')[-1]
                    stock = item.find('span', {'data-test': 'addMessage'})
                    sold_out = False
                    if stock:
                        if stock.text in self.stock_labels:
                            sold_out = True
                    stock = item.find('div', {'data-test': 'LPFulfillmentSection'})
                    if stock:
                        stock = stock.find('span', {'class': 'h-text-grayDark'})
                        if stock:
                            if stock.text in self.stock_labels:
                                sold_out = True
                            else:
                                print(stock.text)
                    stock = item.find('div', {'data-test': 'soldOutMessageLP'})
                    if stock: 
                        if stock.text in self.stock_labels:
                            sold_out = True
                    if not sold_out and sku in self.watched_skus:
                        self.found.append(''.join([self.base_url, item_url]))
                    if sku:
                        self.sku_found += 1
        self.print_results()
            

if __name__ == '__main__':
    search = TargetSearch()