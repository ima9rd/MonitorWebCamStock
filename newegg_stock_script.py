from base_search_class import BaseSearch
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs


class NeweggSearch(BaseSearch):

    def initialize(self):
        self.vendor_name = 'Newegg'
        self.stock_labels = ['OUT OF STOCK']
        self.watched_skus = ['N82E16826104368', 'N82E16826104469', 'N82E16826104648', 'N82E16826197335', '1EF-000C-001J3']
        self.base_url ='https://www.newegg.com'
        self.search_url = 'https://www.newegg.com/p/pl?d=webcam&N=8000'
        self.requires_user_agent = True
        self.search_hierarchy = [
            {'multi': True, 'tag': 'div', 'search': {'class': 'item-container'}}
        ]

    def process_items(self):
        for item in self.items:
            if not item:
                pass
            else:
                item_url = item.a['href']
                sku = parse_qs(urlparse(item_url).query)
                if 'Item' in sku:
                    sku = sku['Item'][0]
                if sku in self.watched_skus:
                    if item.find('p', {'class': 'item-promo'}).get_text() not in self.stock_labels:
                        self.found.append(item_url)
                if sku:
                    self.sku_found += 1
        if len(self.found) > 0:
            print(self.found)
        elif self.sku_found > 0:
            print('Newegg: no items in stock.')
        else:
            print('Newegg: failed to find results.')
            

if __name__ == '__main__':
    search = NeweggSearch()