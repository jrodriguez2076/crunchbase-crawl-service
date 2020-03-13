# Crunchbase Crawler for Company Global traffic ranks
# To start using:
# 1. Copy dataset file into root folder of this project.
# 2. Change 'self.filename' for the dataset filename to use.
# 3. Run command: scrapy crawl crunch
# 
# NOTE: Make sure to have a virtual environment with everything installed from 'requirements.txt'

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv

import pandas as pd
import numpy as np

class CrunchSpider(scrapy.Spider):
        name = "crunch"

        def __init__(self, *args, **kwargs):
            self.companies = []
            self.filename = 'FinalCrunchbaseDataset.csv' #### CHANGE THIS FOR REAL FILENAME
            self.companies = pd.read_csv(self.filename)
            complete_urls = []

            # Prepare all urls to be crawled for this run
            for index, company in self.companies.iterrows():
                if company.GlobalTrafficRank != company.GlobalTrafficRank: # Verify if the value for GlobalTrafficRank is NAN (NAN is never equal to another NAN)
                    complete_url = ('https://www.crunchbase.com/organization/' + company['permalink'] + '#section-web-traffic-by-similarweb', index)
                    complete_urls.append(complete_url)

            self.start_urls = complete_urls
            print('URLs to crawl:', len(complete_urls))

        # Scrapy method for start sending requests
        def start_requests(self):
            urls = self.start_urls
            for count, url in enumerate(urls):
                yield scrapy.Request(url = url[0], callback = self.parse, meta={'itemCount': count})
            
        def parse(self, response):

            # Select the HTML element containing the rank of the company
            extractedHTML = response.css('markup-block').getall()
            RankHTML = ''
            RankStartPos = -1
            request_index = response.meta['itemCount']

            # If several elements are found, check each one to find the element containing the rank, and set the starting position of the rank value
            for selectedElement in extractedHTML:

                RankStartPos = selectedElement.find('is ranked <field-formatter class=\"ng-star-inserted\"><span class=\"component--field-formatter field-type-integer ng-star-inserted\" title=\"')
                if RankStartPos > 0:
                    RankHTML = selectedElement
                    RankStartPos = RankStartPos + len('is ranked <field-formatter class=\"ng-star-inserted\"><span class=\"component--field-formatter field-type-integer ng-star-inserted\" title=\"')
                    break

            # Set the ending position of the rank in the selected HTML
            if RankStartPos > 0:
                RankEndPos = RankHTML.find('">',RankStartPos)
            # try:
                print('{0} out of {1} companies checked'.format(request_index + 1,len(self.start_urls)))
                
                Ranking = int(RankHTML[RankStartPos:RankEndPos].replace(",",""))        
                self.companies.iloc[self.start_urls[request_index][1],self.companies.columns.get_loc('GlobalTrafficRank')] = Ranking
                self.companies.to_csv(self.filename, index=False)
                self.log('Saved in file %s' % self.filename)


