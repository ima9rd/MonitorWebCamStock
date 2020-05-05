from base_search_class import BaseSearch
from bs4 import BeautifulSoup as bs


class StaplesSearch(BaseSearch):

    def initialize(self):
        self.javascript = True
        self.vendor_name = 'Staples'
        self.stock_labels = ['Out of Stock']
        self.watched_skus = ['325807', '445476', '100287', '354562', '869256', '2705146', '325808']
        self.base_url ='https://www.staples.com'
        self.search_url = 'https://www.staples.com/webcam/directory_webcam'
        self.requires_user_agent = True
        self.search_hierarchy = [
            {'multi': True, 'tag': 'div', 'search': {'class': 'nested_grid_content'}}
        ]

    def process_items(self):
        for item in self.items:
            if not item:
                pass
            else:
                item_url = item.find('a', {'class': 'standard-type__product_title'})
                if item_url:
                    item_url = item_url['href']
                    sku = item_url.split('/product_')[1]
                    sold_out = False
                    stock = item.find('div', {'class': 'notification__notification'})
                    if stock:
                        if stock.text in self.stock_labels:
                            sold_out = True
                    if sku in self.watched_skus and not sold_out:
                        self.found.append(''.join([self.base_url, item_url]))
                    if sku:
                        self.sku_found += 1
        if len(self.found) > 0:
            print(self.found)
        elif self.sku_found > 0:
            print('Staples: no items in stock.')
        else:
            print()



if __name__ == '__main__':
    search = StaplesSearch()