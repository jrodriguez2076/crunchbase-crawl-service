import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv


class CrunchSpider(scrapy.Spider):
        name = "crunch"

        def __init__(self, start_urls):
            self.start_urls = start_urls
            pass

        def start_requests(self):
            urls = self.start_urls

            # urls = [
            #         'https://www.crunchbase.com/organization/nine-supply#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/ringmaster-technologies#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/tetra-defense#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/newtropic#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/olive-healthcare#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/worktech-528a#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/mile-share#section-web-traffic-by-similarweb',
            #         'https://www.crunchbase.com/organization/hupro-japan#section-web-traffic-by-similarweb',
            #         ]
            for url in urls:
                yield scrapy.Request(url = url, callback = self.parse)
            
        def parse(self, response):

            # Select a parent element containing the rank of the company
            extractedHTML = response.css('markup-block').getall()
            RankHTML = ''
            RankStartPos = -1

            # If several elements are found, check each one to find the element containing the rank
            for selectedElement in extractedHTML:

                RankStartPos = selectedElement.find('is ranked <field-formatter class=\"ng-star-inserted\"><span class=\"component--field-formatter field-type-integer ng-star-inserted\" title=\"')
                print(RankStartPos)
                if RankStartPos > 0:
                    RankHTML = selectedElement
                    RankStartPos = RankStartPos + len('is ranked <field-formatter class=\"ng-star-inserted\"><span class=\"component--field-formatter field-type-integer ng-star-inserted\" title=\"')
                    break

            if RankStartPos > 0:
                RankEndPos = RankHTML.find('">',RankStartPos)
                try:
                    Ranking = int(RankHTML[RankStartPos:RankEndPos].replace(",",""))        
                    filename = 'ranks.txt'
                    with open(filename, 'a') as f:
                        f.write('%d\n' % Ranking)
                    self.log('Saved in file %s' % filename)

                    # Organization.GlobalTrafficRank = Ranking
                    
                except:
                    print('Failed')
                    pass
            else:
                try:
                    Ranking = 0        
                    filename = 'ranks.txt'
                    with open(filename, 'a') as f:
                        f.write('%d \n' % Ranking)
                    self.log('No Ranking found. Saved in file %s' % filename)
                except:
                    print('Failed')
                    pass