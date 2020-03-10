import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv
from eoty.spiders.crunch_spider import CrunchSpider

companies = []
filename = 'CrunchbaseOutput_900000_999999.csv' #### PUT REAL FILENAME HERE
with open(filename,encoding="utf8") as f:
    csv_data = csv.reader(f, delimiter=',')
    for row in csv_data:
        companies.append(row)

companies.remove(companies[0])

complete_urls = []
for company in companies:
    complete_url = 'https://www.crunchbase.com/organization/' + company[16] + '#section-web-traffic-by-similarweb'
    complete_urls.append(complete_url)

# complete_urls = [
#             'https://www.crunchbase.com/organization/nine-supply#section-web-traffic-by-similarweb',
#             'https://www.crunchbase.com/organization/ringmaster-technologies#section-web-traffic-by-similarweb',
#             'https://www.crunchbase.com/organization/tetra-defense#section-web-traffic-by-similarweb',
#             'https://www.crunchbase.com/organization/newtropic#section-web-traffic-by-similarweb',
#             'https://www.crunchbase.com/organization/olive-healthcare#section-web-traffic-by-similarweb',
#             ]

process = CrawlerProcess(get_project_settings())

process.crawl(CrunchSpider,complete_urls)
process.start()

rankings = []
with open('ranks.txt') as f:
    rankings = f.read().splitlines()

for i,ranking in enumerate(rankings):
    companies[i][9] = ranking

with open('complete_companies.csv', 'w', encoding='utf8') as f:
    f.write(str(companies))