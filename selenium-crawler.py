from selenium import webdriver
import csv
import pandas as pd
import numpy as np
import time
import random
import sys

def webdriver_selection(selectedBrowser):
    if selectedBrowser == 'Firefox':
        return webdriver.Firefox()
    elif selectedBrowser == 'Chrome':
        return webdriver.Chrome('./chromedriver')
    else: 
        return -1

companies = []
filename = str(sys.argv[1])  # 'FinalCrunchbaseDataset-7681.csv' #### CHANGE THIS FOR REAL FILENAME
companies = pd.read_csv(filename)
complete_urls = []
for index, company in companies.iterrows():
    if company.GlobalTrafficRank != company.GlobalTrafficRank: # Verify if the value for GlobalTrafficRank is NAN (NAN is never equal to another NAN)
        complete_url = ('https://www.crunchbase.com/organization/' + company['permalink'] + '#section-web-traffic-by-similarweb', index)
        complete_urls.append(complete_url)
print('URLs to crawl:', len(complete_urls))

browser = webdriver_selection(str(sys.argv[2])) # webdriver.Chrome('./chromedriver')

print(complete_urls[0])
for index,url in enumerate(complete_urls):
    
    print('Now checking URL: ', str(url[0]))
    browser.get(url[0])
    time.sleep(2)
    try:
    
        elem = browser.find_element_by_id("section-web-traffic-by-similarweb")
    
        RankStartPos = elem.text.find('is ranked ') + len('is ranked ')
        # Set the ending position of the rank in the selected HTML
        if RankStartPos > 0:
            print('Got a rank, now storing')
            RankEndPos = elem.text.find(' among',RankStartPos)
            rank = int(elem.text[RankStartPos:RankEndPos].replace(",",""))
            print(rank)
            companies.iloc[complete_urls[index][1],companies.columns.get_loc('GlobalTrafficRank')] = rank
            companies.to_csv(filename, index=False)
            print('{0} out of {1} companies checked'.format(index + 1,len(complete_urls)))
        else: print('No Rank found for this company')
    except:
        print('No Rank found for this company. Checking if it is a bot wall') 
        try:
            buttonFrame = browser.find_element_by_xpath("//h1[contains(string(), 'Please verify you are a human')]")
            if  buttonFrame.text == "Please verify you are a human" :
                input("***************This is a bot wall, Please verify in browser, then press ENTER to continue************")
        except:
            print('No wall, and no rank... moving on')
            pass
print("CRAWL COMPLETED.\nPlease check your input file to review the changes.")
browser.quit()

