import time
from urllib.request import FancyURLopener  # This is library that helps us create the headless browser
from random import choice #This library helps pick a random item from a list
import bs4 as bs
import datetime
from datetime import timedelta, date
import pandas as pd
from selenium import webdriver
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import numpy as np


##def init_browser():
##    executable_path = {'executable_path': 'chromedriver.exe'}
##    return Browser("chrome", **executable_path, headless=False)
from splinter import Browser
from selenium.webdriver.chrome.service import Service

def init_browser():
    path = r'C:\Users\dell\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # <-- use raw string (r'') or double backslashes
    service = Service(executable_path=path)
    return Browser("chrome", service=service, headless=False)



user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.208 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.208 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.2478.80 Chrome/124.0.6367.208 Safari/537.36'
]

class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

# Get each article and their link
def getArticleMeta(infotable):
    for i in range(0,len(infotable)):
        CallDesc.append(infotable[i].getText().encode('utf-8'))
        CallLink.append(infotable[i]['href'])
        
def getDate(i):
    date = i.find("span", class_= "date")
    date = date.getText()
    try:
        date = pd.to_datetime(date,infer_datetime_format=True)
    except ValueError:
        if "Yesterday" in date:
            Date = datetime.date.today() - timedelta(1)
            date = date[10:]
            date = str(Date) + date
        else:
            date = date.split(',')[1]
            date = date + ' ' + str(2017)
        date = pd.to_datetime(date,infer_datetime_format=True)
    return date

#def getTicker(companyName):
#    df = pd.read_csv('company.txt', sep = '\t')
#    df = df[df['Country'] == 'USA']
#    dfD = df.set_index('Name')['Ticker'].to_dict()
#    del df
#    return dfD[process.extractOne(companyName, dfD.keys())[0]]


# This uses the search tool on Seeking Alpha to get pull specific company's transcript.
def getTranscriptBySearch(ticker):
    CallDesc = []
    CallLink = []
    browser = init_browser()
    try:
        ticker = ticker
        url = 'https://seekingalpha.com/search/transcripts?term='+ ticker
        browser.visit(url) # Start the browser and open 'url'
    except KeyError:
        print("That company doesn't exist in my masterlist")
        raise

    assert 'Seeking Alpha' in browser.title # Wait for the page to load
    html = driver.page_source # Get the html of the page
    driver.quit() # Close the browser

    soup = bs.BeautifulSoup(html, 'html.parser')

    infotable = soup.find_all("div", class_= "transcript_link")
    for i in infotable:
        date = getDate(i)
        if (date >= datetime.datetime(2016,9,1)) & (ticker in i.find('a').getText()):
            CallDesc.append(i.find('a').getText().encode('utf-8'))
            CallLink.append(i.find('a')['href'])
    CreateTextFiles(CallLink)



    # get list of S&P 100 companies and tickers from wikipedia

import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

# get the response in the form of html
wikiurl="https://en.wikipedia.org/wiki/S%26P_100"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)


# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')
sandp100=soup.find_all('table')
df=pd.read_html(str(sandp100))

#convert list to dataframe
df=pd.DataFrame(df[2])
print(df.head(25))
df.to_csv('sandp100.csv', index=False)


# This goes into the transcript link and extracts the text from each link
def CreateTextFiles(CallLink):
    for link in range(0,len(CallLink)):
        myopener = MyOpener()
        page=myopener.open('https://seekingalpha.com' + CallLink[link])

        html = page.read()
        soup = bs.BeautifulSoup(html, 'lxml')

        infotable = soup.find_all("p", class_= "p")
        try:
            Output_File = open(str(infotable[0].find("a")['title']) + 
                               str(infotable[2].getText()) + ".txt",'w')
        except IndexError as exc:
            continue
        except TypeError as typ:
            continue

        for i in range(0,len(infotable)):
            if(infotable[i].getText().encode('utf-8').startswith('Copyright policy:')):
                break
            if(len(infotable[i].getText()) == 0):
                time.sleep(600)
                continue
            Output_File.write(infotable[i].getText().encode('utf-8'))
            Output_File.write("\n")
        Output_File.close()

import re
import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

url = 'https://seekingalpha.com/symbol/AAPL/transcripts'
browser = init_browser()
browser.visit(url)
time.sleep(10)
html = browser.html
soup = bs(html, "html.parser")
results = soup.find_all("article")

for result in results:
    title = result.find('h3').text.strip()
    transcript_url = result.find('a')['href']
    date_str = result.find('span').text.strip()
    
    # Check if date string contains a 4-digit year before converting
    if re.search(r'\b\d{4}\b', date_str):
        try:
            date = pd.to_datetime(date_str, infer_datetime_format=True)
            if date > datetime.datetime(2022, 1, 1):
                print(title)
                print(transcript_url)
                print(date)
        except Exception as e:
            print(f"Skipping invalid date '{date_str}': {e}")
    else:
        print(f"Skipping date without year: {date_str}")

    


def getTranscriptInfo(ticker, browser_):   
    url = 'https://seekingalpha.com/symbol/' + ticker + '/transcripts'
    browser = browser_
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find_all("article")
    search_results = []
    for result in results:
        try:
            title = result.find('h3').text
            url = result.find('a')['href']
            date = result.find('span').text
            date = pd.to_datetime(date,infer_datetime_format=True)
            if (date > datetime.datetime(2022, 1, 1)):
                print(title)
                print(url)
                print(date)
                print('----------------------------------------')
                results_dict = {
                    "title": title,
                    "url": url,
                    "date": date,
                    "ticker": ticker
                }
                search_results.append(results_dict)
        except:
            continue
    return search_results

browser = init_browser()
getTranscriptInfo('AAPL', browser)


all_results = []
df = pd.read_csv('sandp100.csv', usecols = ['Symbol'])
tickers = df['Symbol'].tolist()
browser = init_browser()
for ticker in tickers:
    counter = 0
    results = getTranscriptInfo(ticker, browser)
    all_results = all_results + results
    time.sleep(5)
    
    

df_all = pd.DataFrame(all_results)

df_all.to_csv('transcript_list.csv', index=False)
def getTextFromArticle(url, browser_):
    url_begin = 'https://seekingalpha.com/'
    url_end = url
    browser = browser_
    browser.visit(url_begin+url_end)
    time.sleep(10)
    html = browser.html
    soup = bs(html, "html.parser")
    texts = soup.find_all('p')
    total_doc = ''
    for text in texts:
        total_doc += text.text + '\n'
    return total_doc

texts = soup.find_all('p')
total_doc = ''
for text in texts:
    total_doc += text.text + '\n'
print(total_doc)
    
df_all = pd.read_csv("transcript_list.csv")
df_ECT = df_all[df_all['title'].str.contains("Earnings Call Transcript")]
df_ECT["text"] = np.nan
df_ECT

