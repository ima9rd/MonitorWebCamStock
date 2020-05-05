import bestbuy_stock_script
import newegg_stock_script
import staples_stock_script
import target_stock_script


if __name__ == '__main__':
    bb = bestbuy_stock_script.BestBuySearch()
    ne = newegg_stock_script.NeweggSearch()
    st = staples_stock_script.StaplesSearch()
    ta = target_stock_script.TargetSearch()