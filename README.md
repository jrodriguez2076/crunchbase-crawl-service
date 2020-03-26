# crunchbase-crawl-service


This project contains crawling methods to extract data from crunchbase. 

In this instance, crawlers extract companies rank according to the traffic they get from their website. The crawlers read companies from a .csv file and after getting the company rank, it is stored in the GlobalTrafficRank column.

### There are two crawling methods for getting the data:

- SCRAPY SPIDER: A Spider receives all URLs coming from the csv file and begins crawling, while rotating User Agents and Proxies to bypass bot walls. Better suited when searching for several companies, as it can work unmonitored.

- SELENIUM CRAWLER: A crawler implemented using Selenium Browser Automation library, as a way to perform faster crawling of the data. This works better when searching for a smaller number of companies (between 50-100), as it cannot bypass the bot walls yet. Therefore, it can only work monitored for longer sets of URLs (The user must pass the human verification check page). Can run on Firefox and Chrome.

NOTE: There is also a Proxies Extractor module included, that searches for valid Proxies from https://free-proxy-list.net/ and includes them in the spider, to make sure that there are always valid IP addresses to use.

### How to run the crawlers:

to run the crawlers perform the following:

1. Create a new virtual environment, activate it, and run:

		pip install -r requirements.txt

2. Create a .csv file in the root folder of the project containing at least the company name, the company permalink, and an empty column named "GlobalTrafficRank". A sample file is included. Try to avoid using Excel to edit it, as it can create issues with the crawlers. Use pandas to generate new csv files from dataframes instead (or edit the file via text editor).

3. run the following command:

		python crunchbase_service.py
		
4. Enter your input file name when prompted

5. Select your preffered crawling method. If selenium is selected, you will be prompted to choose your preffered browser.

6. Wait until crawling is complete and check your input file for the data.

### ADDITONAL NOTES:

- Don't move your input file after starting the crawl. Your input file is being populated with the data gathered AFTER EACH CRAWL. this is to ensure that it can safely store the data in case a force interrupt must be performed by the user. This will also help when restarting the crawl, since it will only read the lines that don't have their GlobalTrafficRank column populated.
	
- The crawlers will give feedback of their status if there was a successful scrap of the URL. do note that NOT ALL COMPANIES HAVE A GLOBAL TRAFFIC RANK, so some of the fields might still be empty after crawling is complete.
