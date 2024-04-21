from bs4 import BeautifulSoup as bs
import bs4
import requests,json
import pandas as pd
import time,gc,sys
from os import path

# To send a request for page
def page_request(page=0,url=None): 
    if(page!=0):
        url = 'https://www.business-standard.com/finance/news/page-'+ str(page)
    return requests.get(url,headers={'User-Agent':'Microsoft Edge/119.0'})


# To scrape the headlines
def fetchHeadlines(r,df,lvl=0,counter=0,page=1,pass_buffer_df=None):
              
    buffer_df = pd.DataFrame(data={'headlines':'Empty','content':'Empty','img_link':'Empty'},index=[0])
    if(counter!=0):
        buffer_df = pass_buffer_df.copy(deep=True)
    soup = bs(r.content,'lxml')
    for container in soup.find_all('a',attrs={'class':'smallcard-title'}):
        if lvl > 49:
            break
        link = container['href']
        if (path.exists('./Data/news/news_in_jsonFile.json')):     # Here also checks the existence of the json file in our directory

            if(df.loc[0,'headlines']!=container.string):
                resp = fetchContents(link,lvl,df=buffer_df,counter=counter,refresh_msg=True)
                if(resp=='R' or resp=="RR"):
                    continue
                buffer_df.loc[counter,'headlines'] = container.string
                counter = counter + 1
                if(counter == 50):
                    df = buffer_df.copy(deep=True)
    
            if(df.loc[0,'headlines']==container.string):
                if(counter!=0):
                    buffer_df = pd.concat([buffer_df,df],ignore_index=True)
                    if(len(df.index) + len(buffer_df.index) > 50):
                        buffer_df = buffer_df.drop([x for x in range (50,len(buffer_df.index))])
                    df = buffer_df.copy(deep=True)
                lvl = 50
                break  

        else:
            df.loc[lvl,'headlines'] = container.string         
            resp = fetchContents(link,lvl,df=df)
            if(resp == 'R' or resp == "RR"):
                continue
            counter = counter + 1
        lvl = lvl + 1

    if(lvl < 50):
        return fetchHeadlines(page_request(page+1),df,lvl,counter,page+1,pass_buffer_df=buffer_df)
    return counter,df

# To scrape contents of the respective headlines
def fetchContents(content_link,lvl,df,counter=None,refresh_msg=False):

    def gen():          
        a = ['\r','\n','\t']
        yo = iter(a)
        for i in range(len(a)):
            yield next(yo)
    def ES_remover(text):
        for j in gen():
            text = text.replace(j,'')
        return text
    r = page_request(url=content_link)
    content_parser = bs(r.content,'lxml')
    content = content_parser.find('div',attrs = {'class':'MainStory_storydetail__uDFCx'})
    img_content = content_parser.find('div',attrs={'class':'MainStory_positionrelative__jOIzS'}).img
    img_link = img_content['src']
    img_link = img_link[:img_link.find('?'):]
    content_chunk = []
    find_pre = content_parser.find('div',class_='MainStory_strlabel__iEDZ4')
    content = content.find('div',class_ = 'MainStory_storycontent__Pe3ys')
    try:
        if(find_pre.get_text() == " Premium "):
                 return 'R'                              # 'R' is RED alert for premium news
    except Exception:
        return "RR"
    del find_pre
    for refined_contents in content.find_all('div'):
        buffer_content_chunk = ""
        if len(refined_contents.attrs.keys())==0 :
            for i in refined_contents.children:
                if type(i) == bs4.element.NavigableString or i.name in ['a','em','strong']:
                    buffer_content_chunk= buffer_content_chunk + ES_remover(i.get_text())
            content_chunk.append(buffer_content_chunk)
    if(refresh_msg==True):
        df.loc[counter,'content'] = content_chunk
        df.loc[counter,'img_link'] = str(img_link)
    else:
        df.loc[lvl,'content'] = content_chunk
        df.loc[lvl,'img_link'] = str(img_link)


# Calling this method starts the Scraping of newses from Finance News page of Business Standard news website
def igniteScrap():

    if(path.exists('./Data/news/news_in_jsonFile.json')):                          #Checks the existence of the json file
        df = pd.read_json('./Data/news/news_in_jsonFile.json',orient='records')    #Loads the json file from the directory where we have STORED it
    else:                                       
        df = pd.DataFrame(data={'headlines':'NaN','content':'NaN','img_link':'NaN'},index=[0])
    counter,df=fetchHeadlines(page_request(1),df)
    for DataInstance in df.iterrows():
        NewsInstance = dict(DataInstance[1])
        while(NewsInstance['content'].count("") != 0):
            NewsInstance['content'].remove("")
        df.iloc[DataInstance[0],1] = NewsInstance['content']
    if counter > 0 :                
        df.to_json("./Data/news/news_in_jsonFile.json",orient="records",indent=1)  #change the path where you want json file to be STORED
        # print("Scraper] : File Updated",end="\n\n")
    del df
    # print("[Scraper] : News Scraped = {}".format(counter),end="\n\n")


igniteScrap()       #We must call it from another program to execute the scraping and loading the JSON file into the specified directory
