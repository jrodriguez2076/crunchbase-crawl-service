from selenium import webdriver
import csv
import pandas as pd
import numpy as np
import time
import random
# from proxiesExtractor import get_proxies

# proxy_list = get_proxies()

companies = []
filename = 'FinalCrunchbaseDataset-7681.csv' #### CHANGE THIS FOR REAL FILENAME
companies = pd.read_csv(filename)
complete_urls = []
for index, company in companies.iterrows():
    if company.GlobalTrafficRank != company.GlobalTrafficRank: # Verify if the value for GlobalTrafficRank is NAN (NAN is never equal to another NAN)
        complete_url = ('https://www.crunchbase.com/organization/' + company['permalink'] + '#section-web-traffic-by-similarweb', index)
        complete_urls.append(complete_url)
print('URLs to crawl:', len(complete_urls))
# print( 'Proxies to use: ', len(proxy_list))


# current_proxy = random.choice(proxy_list)
# webdriver.DesiredCapabilities.CHROME['proxy']={
#     "httpProxy":current_proxy,
#     "ftpProxy":current_proxy,
#     "sslProxy":current_proxy,
    
#     "proxyType":"MANUAL",
    
# }

browser = webdriver.Chrome('./chromedriver')

print(complete_urls[0])
# changeProxy = False
for index,url in enumerate(complete_urls):
    # if changeProxy == True:
    #     current_proxy = random.choice(proxy_list)
    #     webdriver.DesiredCapabilities.CHROME['proxy']={
    #         "httpProxy":current_proxy,
    #         "ftpProxy":current_proxy,
    #         "sslProxy":current_proxy,
            
    #         "proxyType":"MANUAL",
            
    #     }

    #     browser = webdriver.Chrome('./chromedriver')
    
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
            print('buttonFrame: ', buttonFrame.text)
            if  buttonFrame.text == "Please verify you are a human" :
                # current_proxy = random.choice(proxy_list)
                # webdriver.DesiredCapabilities.CHROME['proxy']={
                #     "httpProxy":current_proxy,
                #     "ftpProxy":current_proxy,
                #     "sslProxy":current_proxy,
                    
                #     "proxyType":"MANUAL",
                    
                # }
                # print("bot wall found. Changing proxy..." )
                # changeProxy = True
                input("***************This is a bot wall, Please verify in browser, then press ENTER to continue************")
        except:
            print('No wall, and no rank... moving on')
            pass


# <div id="dbrdyfUGuHofVBe" role="main" aria-label="Human Challenge requires verification. Please press and hold the button until verified"><div id="RyAUPelzhTnLueg" style="width: 0px;"></div><p id="uNUtWpDmZybzBjJ" class="qYhAtpgfWcRhIrP" style="animation: 81.7333ms ease 0s 1 normal none running textColorIReverse;">Press &amp; Hold</p><div class="fetching-volume"><span>•</span><span>•</span><span>•</span></div><div id="checkmark"></div><div id="ripple"></div></div>