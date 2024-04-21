
from selenium.webdriver import Edge
from selenium.webdriver import EdgeOptions                          #added this part
from selenium.webdriver.edge.service import Service                 #added this part
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests as re
import json


def phase1(driver,stock_data):
    # print(stock_data)
    PerformanceStainerObj = SoupStrainer(attrs={"class":"block-sjmalUvv"})
    PerformanceSoupObj = bs(driver.page_source,"lxml",parse_only=PerformanceStainerObj)
    PerformanceSoupObj = PerformanceSoupObj.contents[0]
    # print(PerformanceSoupObj.contents[1].prettify())
    stock_data["performance"]["one_week"] = PerformanceSoupObj.contents[1].span.contents[1].get_text().replace('%','')
    stock_data["performance"]["one_month"] = PerformanceSoupObj.contents[2].span.contents[1].get_text().replace('%','')
    stock_data["performance"]["six_months"] = PerformanceSoupObj.contents[3].span.contents[1].get_text().replace('%','')
    performance_list = list(stock_data['performance'].keys())
    for i in range (len(performance_list)):
        if '−' in stock_data['performance'][performance_list[i]]:
            stock_data['performance'][performance_list[i]] = '-' + stock_data['performance'][performance_list[i]].strip('−')
        stock_data['performance'][performance_list[i]] = float( stock_data['performance'][performance_list[i]])
    del PerformanceSoupObj,PerformanceStainerObj
    return phase2(driver,stock_data)

def phase2(driver,stock_data):
    # print(stock_data)
    KeystatsStainerObj = SoupStrainer(name="div",attrs={"class":"container-GRoarMHL"})
    KeystatsSoupObj = bs(driver.page_source,"lxml",parse_only=KeystatsStainerObj)
    KeystatsSoupObj = KeystatsSoupObj.contents[0]
    # print(KeystatsSoupObj.prettify())
    stock_data_keys = list(stock_data.keys())
    keystatsIndex = 0
    stock_data_keysIndex = keystatsIndex + 1
    KeystatChild = KeystatsSoupObj.contents[0]
    while(keystatsIndex < len(KeystatsSoupObj.contents) - 1):
        if(keystatsIndex == 3):
            keystatsIndex += 1
            continue
        stock_data[stock_data_keys[stock_data_keysIndex]] = KeystatsSoupObj.contents[keystatsIndex].contents[1].div.get_text().replace('INR','')
        # INR_index = stock_data[stock_data_keys[stock_data_keysIndex]].find("INR")
        # if(INR_index != -1):
        #     stock_data[stock_data_keys[stock_data_keysIndex]] = stock_data[stock_data_keys[stock_data_keysIndex]][:INR_index:]
        stock_data_keysIndex += 1
        keystatsIndex +=1
    del KeystatsSoupObj,KeystatsStainerObj
    return phase3(driver,stock_data)

def phase3(driver,stock_data):
    # print(stock_data)
    AboutStainerObj = SoupStrainer(attrs={"class":"content-gdSWdaJr"})
    AboutSoupObj = bs(driver.page_source,"lxml",parse_only=AboutStainerObj)
    AboutSoupObj = AboutSoupObj.contents[0]
    AboutKeys = list(stock_data["about"].keys())
    UpperAbout = AboutSoupObj.contents[0]
    try:
        for i in range(len(UpperAbout.contents)):                                #changed this part totally
            Aboutkeyreference = UpperAbout.contents[i].div.get_text() 
            if(Aboutkeyreference in AboutKeys):
                stock_data['about'][Aboutkeyreference] = UpperAbout.contents[i].contents[1].get_text()
    finally:
        stock_data["about"]["desc"] = AboutSoupObj.contents[1].div.get_text()
        del AboutSoupObj,AboutStainerObj
        DataPreviewStainerObj = SoupStrainer(name="div",attrs={"class":["container-pAUXADuj containerWithButton-pAUXADuj"]})
        DataPreviewSoupObj = bs(driver.page_source,"lxml",parse_only=DataPreviewStainerObj)
        DataPreviewSoupObj = DataPreviewSoupObj.contents[0]
        stock_data["data_preview"]["stock_image"] = DataPreviewSoupObj.div.img['src']
        stock_data["data_preview"]["company"] = DataPreviewSoupObj.h1.string
        stock_data["data_preview"]["stock_price"] = float(DataPreviewSoupObj.contents[3].div.div.div.span.get_text())
        stock_data["data_preview"]["symbol_change"] = DataPreviewSoupObj.contents[3].div.div.contents[1].span.get_text()
        stock_data["data_preview"]["symbol_change_pt"] = DataPreviewSoupObj.contents[3].div.div.contents[1].contents[1].get_text().replace('%','')
        symbol = ['symbol_change','symbol_change_pt']
        stock_data['div_yield'] = float(stock_data['div_yield'].replace('%',''))
        for i in range(len(symbol)):
            if '−' in stock_data['data_preview'][symbol[i]] :
                stock_data['data_preview'][symbol[i]] = '-' + stock_data['data_preview'][symbol[i]].strip('−')
            stock_data['data_preview'][symbol[i]] = float(stock_data['data_preview'][symbol[i]])
        return stock_data


def StockDetail(stock_symbol):

    try:
        URL = "https://www.tradingview.com/symbols/"+ stock_symbol.upper()      #Takes the symbol to fetch the data from 

        DRIVER_PATH = 'WebDriver\edgedriver_win64\msedgedriver.exe'             #added this part
        services = Service(executable_path=DRIVER_PATH)                         #added this part
        options =  EdgeOptions()                                                #added this part
        options.add_argument("--headless=new")                                  #added this part
        driver = Edge(options=options,service=services)                         #added this part
        # driver.minimize_window()
        driver.get(URL)
        stock_data = {"performance":{"one_week":None,"one_month":None,"six_months":None},"mrkt_capita":None,"div_yield":None,"PE_ratio":None,"Net_income":None,"Revenue":None,"Share_float":None,"about":{"Sector":None,"Industry":None,"CEO":'-',"Website":None,"Headquarters":None,"Employees (FY)":None,"Founded":None,"ISIN":None,"FIGI":None,"desc":None},"data_preview":{"stock_image":None,"company":None,"stock_price":None,"symbol_change":None,"symbol_change_pt":None}}

        stock_data = phase1(driver,stock_data)
    finally:
        driver.quit()
        return stock_data

    return small_chunk