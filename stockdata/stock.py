from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests as req
import pandas as pd
import json

def page_request():
    return req.get("https://www.tradingview.com/markets/stocks-india/market-movers-large-cap/", headers={"User-Agent": "Microsoft Edge/119.0", "Referer": "https://www.tradingview.com/markets/stocks-india/market-movers-large-cap/"})

def RowExtraction(stock_row):
    small_chunk = {
        "stock_image": None,
        "stock_name": None,
        "company": None,
        "market_cap": None,
        "price": None,
        "change": None,
        "volume": None,
        "rel_volume": None,
        "price_to_earn": None,
        "EPS_dil": None,
        "EPS_dil_growth": None,
        "div_yield": None,
        "sector": None,
    }
    TD_tag = stock_row.find("td")
    if TD_tag.span.contents[1].name == "img":
        small_chunk["stock_image"] = TD_tag.span.img['src']
    small_chunk["stock_name"], small_chunk["company"] = TD_tag.a.string, TD_tag.sup.string
    TD_tag = TD_tag.next_sibling
    small_chunk["market_cap"] = TD_tag.get_text().replace(" INR", "")
    TD_tag = TD_tag.next_sibling
    price_text = TD_tag.get_text().replace(",", "").replace(" INR", "").replace("\u202f", "").replace("−", "-")
    small_chunk["price"] = float(price_text) if price_text and price_text != '—' else None
    TD_tag = TD_tag.next_sibling
    change_text = TD_tag.get_text().replace("%", "").replace("−", "-")
    small_chunk["change"] = float(change_text) if change_text and change_text != '—' else None
    TD_tag = TD_tag.next_sibling
    small_chunk["volume"] = TD_tag.contents[0]
    TD_tag = TD_tag.next_sibling
    small_chunk["rel_volume"] = TD_tag.contents[0]
    TD_tag = TD_tag.next_sibling
    small_chunk["price_to_earn"] = TD_tag.contents[0]
    TD_tag = TD_tag.next_sibling
    small_chunk["EPS_dil"] = TD_tag.contents[0]
    TD_tag = TD_tag.next_sibling
    EPS_dil_growth_text = TD_tag.get_text().replace("%", "").replace("−", "-")
    small_chunk["EPS_dil_growth"] = float(EPS_dil_growth_text) if EPS_dil_growth_text and EPS_dil_growth_text != '—' else None
    TD_tag = TD_tag.next_sibling
    div_yield_text = TD_tag.contents[0].replace("%", "").replace("−", "-")
    small_chunk["div_yield"] = float(div_yield_text) if div_yield_text and div_yield_text != '—' else None
    TD_tag = TD_tag.next_sibling
    small_chunk["sector"] = TD_tag.a.string
    return small_chunk

def start(page_number=1, per_page=10):
    response = page_request()
    StocksData = []
    TablecontainerParent = SoupStrainer(name="table", attrs={"class": "table-Ngq2xrcG"})
    TablecontainerParenttag = bs(response.content, "lxml", parse_only=TablecontainerParent)
    
    # Calculate the starting and ending indices based on page_number and per_page
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page
    
    # Loop through only the required rows based on pagination
    for Stockrows in TablecontainerParenttag.tbody.find_all(name="tr")[start_index:end_index]:
        small_chunk = RowExtraction(Stockrows)
        StocksData.append(small_chunk)
    
    return StocksData

# Start the data extraction process
stocks_data = start()

# Print the extracted data

