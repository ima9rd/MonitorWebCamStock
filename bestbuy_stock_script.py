from base_search_class import BaseSearch
from bs4 import BeautifulSoup as bs


class BestBuySearch(BaseSearch):

    def initialize(self):
        self.vendor_name = 'BestBuy'
        self.stock_labels = ['Check Stores', 'Sold Out']
        self.watched_skus = ['2588445', '6366565', '4612476', '6321794', '6404199', '5579380', '9928354', '4503702', '5761912', '6289641']
        self.base_url ='https://www.bestbuy.com'
        self.search_url = 'https://www.bestbuy.com/site/searchpage.jsp?st=webcam'
        self.search_hierarchy = [
            {'multi': True, 'tag': 'div', 'search': {'class': 'shop-sku-list-item'}}
        ]

    def process_items(self):
        for item in self.items:
            if not item:
                pass
            else:
                item_url = item.find('h4', {'class': 'sku-header'}).a['href']
                sku = item.find(attrs={'class': 'list-item'})['data-sku-id']
                if sku in self.watched_skus:
                    if item.find('button', {'class': 'add-to-cart-button'}).get_text() not in self.stock_labels:
                        self.found.append(''.join([self.base_url, item_url]))
                if sku:
                    self.sku_found += 1
        if len(self.found) > 0:
            print(self.found)
        elif self.sku_found > 0:
            print('BestBuy: no items in stock.')
        else:
            print('BestBuy: failed to find results, including test SKU.')


if __name__ == '__main__':
    search = BestBuySearch()