import os
import time

browserList = [
    'Firefox',
    'Chrome',
]

if __name__ == "__main__":
    filename = input("Welcome. Please enter your file name below (MUST be .csv file):\n" )
    filename = filename + '.csv'
    option = input("Please choose a crawling method:\n\n [1] Unmonitored (Scrapy. Takes longer to crawl all sites)\n\n [2] Monitored (Selenium. Faster, but requires human verification\n\n [3] Exit\n\n Your Choice: ")
    

    if option == "1":
        print("Scrapy Crawler selected. Starting now...")
        time.sleep(1)
        os.system('scrapy crawl crunch -a filename={}'.format(filename))
    elif option == "2":
        print("Selenium Crawler selected. Please choose your preferred Browser for crawling:")
        for i,value in enumerate(browserList):
            print("[" + str(i + 1) + "] " + value + "\n")
        browser = browserList[int(input("Your choice: ")) - 1]
        time.sleep(1)
        os.system('python selenium-crawler.py {0} {1}'.format(filename, browser))
    elif option == "3":
        exit()
    else:
        print("Error, please select an option from the menu\n")