# MonitorWebCamStock
Simple Python scripts to scrape and parse search results for various online retailers and check for webcams that are in stock. Note: BestBuy stock status is unreliable. Some items report as in stock until you attempt checkout, so do not always rely on these results alone.

The basic approach is to create a search hierarchy of tag, {attribute: value}, then extend BaseSearch.process_items to handle vendor-specific result structures for items. This script handles websites that use JavaScript/React by using selenium to load the page in the background and check for certain elements/scrolling to the bottom to force the page to load.

This script requires ChromeDriver.exe to be placed in the same folder as search.py. This file can be found here - https://chromedriver.chromium.org/.
