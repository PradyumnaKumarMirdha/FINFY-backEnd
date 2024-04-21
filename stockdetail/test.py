
from selenium.webdriver import Edge
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import WebDriverException
import json 

# To be started
PATH = '.\WebDriver\edgedriver_win64\msedgedriver.exe'
URL = 'https://in.tradingview.com/screener/'
GMAIL_ID = 'finfy44@gmail.com'
PASS = 'Finfy@2024'
TURN = 1

StockData = {'stock_image':None,'company':None,'stock_symbol':None,'price':None,'change(pt)':None,'change':None,'volume':None,'rel_volume':None,'mrkt_cap':None,'p/e':None,'div_yield(pt)':None,'sector':None,'high24H':None,'low24H':None,'1week_perf(pt)':None,'1mon_perf(pt)':None,'3mon_perf(pt)':None,'1yr_perf(pt)':None,'total_assets':None,'total_assets_growth':None}

class EdgeDriver:
    def __init__(self,options,services):
        self.options = options
        self.services = services
        self.driver = None
    def __enter__(self):
        self.driver = Edge(service=self.services,options=self.options)
        return self.driver
    def __exit__(self):
        self.driver.quit()

# def StartDriver():
#     #adding options
#     options = EdgeOptions()
#     options.page_load_strategy="normal"
#     # options.add_argument("--headless=new")

#     #Adding services to the driver
#     service = Service(executable_path=PATH)

#     #Initializing the driver with MSEDGE driver
#     driver = Edge(service=service,options=options) 
#     driver.maximize_window()
#     return driver


#Takes us to the Sign-IN page
def MovingToSignInPage(driver,parent_window):
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//button[@aria-label='Open user menu']")))
    driver.find_element(By.XPATH,"//button[@aria-label='Open user menu']").click()
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//button[@class='item-jFqVJoPk item-mDJVFqQ3']")))
    driver.find_element(By.XPATH,"//button[@class='item-jFqVJoPk item-mDJVFqQ3']").click()
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='googleButton-nKAw8Hvt']")))
    driver.find_element(By.XPATH,"//div[@class='googleButton-nKAw8Hvt']").click()
    child_window_handles = driver.window_handles

    for window_handle in child_window_handles:
        if window_handle != parent_window:
            driver.switch_to.window(window_handle)
            break


#clicking the NEXT button
def ClickOnNext(driver):
    button_instances = driver.find_elements(By.XPATH,"//span[@class='VfPpkd-vQzf8d']")
    i = 1
    for next_button in button_instances:
        if i == 4:
            next_button.click()
            break
        i += 1


# Signing In using the Gmail and the Password
def Signing_In(GMAIL_ID,PASS,driver):
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//input[@class='whsOnd zHQkBf']")))
    # sleep(7)
    driver.find_element(By.XPATH,"//input[@class='whsOnd zHQkBf']").send_keys(GMAIL_ID)
    # sleep(2.5)
    ClickOnNext(driver)
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
    # sleep(5)
    driver.find_element(By.XPATH,"//input[@type='password']").send_keys(PASS)
    # sleep(2.5)
    ClickOnNext(driver)

def fetch_stock_data(driver):
    EarlyStockData = []
    strainer_obj = SoupStrainer(name='table',attrs={'class':'table-Ngq2xrcG'})
    table_element = bs(driver.page_source,"lxml",parse_only=strainer_obj)
    table_content = table_element.tbody
    i = 1
    for row in table_content.contents:
        StockData['stock_symbol'] = row['data-rowkey'].replace(':','-')
        print(f"row no. :{i}\nstock_symbol:{StockData['stock_symbol']}")
        if row.contents[0].span.contents[1].name == 'img':
             StockData['stock_image'] = row.contents[0].span.img['src']
        StockData['company'] = row.contents[0].span.sup.get_text()
        StockData['price'] = float(row.contents[1].next_element)
        if row.contents[2].get_text() != "—":
            StockData['change(pt)'] = row.contents[2].span.next_element.replace("%","")
            if '−' in StockData['change(pt)']:
                StockData['change(pt)'] = '-' + StockData['change(pt)'].strip('−')
            StockData['change(pt)'] = float(StockData['change(pt)'])
        if row.contents[3].get_text() != "—":
            StockData['volume'] = row.contents[3].get_text().split()
            StockData['volume'][0] = float(StockData['volume'][0])              #float parsing
        if row.contents[4].get_text() != "—":
            StockData['rel_volume'] = float(row.contents[4].get_text())         #float parsing
        StockData['mrkt_cap'] = row.contents[5].next_element.split()
        StockData['mrkt_cap'][0] = float(StockData['mrkt_cap'][0])          #float parsing
        if row.contents[6].next_element != "—":
            StockData['p/e'] = float(row.contents[6].next_element)
        StockData['div_yield(pt)'] = float(row.contents[7].get_text().replace('%',''))          #float parsing
        StockData['sector'] = row.contents[8].get_text()
        StockData['high24H'] = float(row.contents[9].next_element)
        StockData['low24H'] = float(row.contents[10].next_element)
        StockData['1week_perf(pt)'] = row.contents[11].get_text().replace('%','')
        StockData['1mon_perf(pt)'] = row.contents[12].get_text().replace('%','')
        StockData['3mon_perf(pt)'] = row.contents[13].get_text().replace('%','')
        StockData['1yr_perf(pt)'] = row.contents[14].get_text().replace('%','')
        performance_list = ['1week_perf(pt)','1mon_perf(pt)','3mon_perf(pt)','1yr_perf(pt)']
        for i in range(len(performance_list)):
            if '−' in StockData[performance_list[i]]:
                StockData[performance_list[i]] = '-' + StockData[performance_list[i]].strip('−')
            StockData[performance_list[i]] = float(StockData[performance_list[i]])
        if row.contents[15].get_text() != "—":
            StockData['change'] = row.contents[15].span.next_element
            if '−' in StockData['change']:
                StockData['change'] = '-' + StockData['change'].strip('−')
            StockData['change'] = float(StockData['change'])
        if row.contents[16].next_element != "—":
            StockData['total_assets'] = row.contents[16].next_element.split()
            StockData['total_assets'][0] = float(StockData['total_assets'][0])
        if row.contents[17].get_text().isalnum() == True:
            StockData['total_assets_growth'] = row.contents[17].get_text().replace('%','')
            if '−' in StockData['total_assets_growth']:
                StockData['total_assets_growth'] = '-' + StockData['total_assets_growth'].strip('−')
            StockData['total_assets_growth'] = float(StockData['total_assets_growth'])
        bufferData = StockData.copy()
        EarlyStockData.append(bufferData) 
        i +=1
        # return
        print(StockData)
    return EarlyStockData

def func():
    
    options = EdgeOptions()
    options.page_load_strategy="normal"
    options.add_argument("--headless=new")

    #Adding services to the driver
    services = Service(executable_path=PATH)
    with EdgeDriver(options = options,services=services) as driver:
        #Requesting the URL in the browser "—"
        # driver.maximize_window()
        # driver.minimize_window()
        driver.get(URL)

        parent_window = driver.current_window_handle
        MovingToSignInPage(driver,parent_window)

        Signing_In(GMAIL_ID=GMAIL_ID,PASS=PASS,driver=driver)
        driver.switch_to.window(parent_window)
        # if len(driver.window_handles) > 1:
        #     print("More than 1 tab is present LOOK OUT")

        sleep(5)        #donot change the sleep time and following sleep times
        driver.find_element(By.XPATH,"//div[@data-name='screener-topbar-screen-title']").click()            #this clicks the stock screener dropdown menu

        sleep(5)
        driver.find_element(By.XPATH,"//div[@class='item-QskOCCG7 popupItem-QskOCCG7 item-jFqVJoPk']").click()      #this clicks the saved custom stock screener
        sleep(5)

        try:
            while True:
                EarlyStockData = fetch_stock_data(driver)
                with open('stock_screener_data.json','w',encoding='utf-8') as file:
                    file.write(json.dumps(EarlyStockData,indent=3))
                sleep(10)
                print("After sleep")
        except KeyboardInterrupt:
            driver.quit()
try:
    func()
except KeyboardInterrupt:
    print("Stopped Abruptly")

#WebDriver exception --- selenium.common.exceptions.WebDriverException
#Timeout Exception can arise and we can't do anything about it, We have to restart the program again
