# Web Scraper script
#By Fher Rodriguez 

from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as req 
from urllib.request import FancyURLopener
import csv
import time, sched
from datetime import date, datetime
import os

mySched = sched.scheduler(time.time, time.sleep)
usrChoice = ""
while True:
    usrChoice = input('Enter "scrape" if you want to scrape and add to the current data or "clear" if you want to erase the current data: ')
    if usrChoice == 'scrape' or usrChoice == 'clear':
        break
    else:
        print('Please enter either "scrape" or "clear" to continue.')
        continue


def scrape():
    timestamp = datetime.now()
    timeStamp_string = timestamp.strftime("%b-%d-%Y %H:%M:%S")

    print('timeStamp: '+timeStamp_string+'\n')

    class myOpener(FancyURLopener):
        version = 'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)'    #Replace the string with your user agent

    opener = myOpener()

    myUrl = 'https://finance.yahoo.com/trending-tickers'

    myClient = opener.open(myUrl)
    mySoup = soup(myClient.read(), features = 'html.parser')
    myClient.close()


    #----------------------------------PARSE YOUR SOUP BELLOW----------------------------------#
    dataContainers = mySoup.findAll('tr')
    print('cont size: '+str(len(dataContainers)))
    print(dataContainers[2].td.text)



    # ------------Un-comment 4 lines bellow to save a copy of the web site HTML--------------#
    # soupHTML = open('soupHTML.html', 'w')
    # for line in mySoup.prettify(formatter = 'minimal'):
    #     soupHTML.write(str(line))
    # soupHTML.close()


    # -------------Un-comment line below to save a CSV file with your scrapped data-------------#
    with open('stock-scraper/data/TrendingStocksToday.csv', 'w', newline="", encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['time stamp', 'symbol', 'name', 'Last Price', 'Market Time', 'Change', '%Change', 'Volume', 'Avg Vol(3month)', 'Market Cap'])   #Fill in with the tags of the CSV#
        for i in range(1,len(dataContainers)-1):
            if dataContainers[i].find('td', {'class':'data-col0 Ta(start) Pstart(6px) Pend(15px)'}).text == ':entitySlug':
                print('this was i before: '+str(i))
                i += 1
                print("found entitySlug, i is: "+str(i))
            cSymbol = dataContainers[i].find('td', {'class':'data-col0 Ta(start) Pstart(6px) Pend(15px)'})
            print(cSymbol.text)
            cName = dataContainers[i].find('td', {'class':'data-col1 Ta(start) Pstart(10px) Miw(180px)'})
            print(cName.text)
            cLastPrice = dataContainers[i].find('td', {'class':'data-col2 Ta(end) Pstart(20px)'})
            print(cLastPrice.text)
            cMarketTime = dataContainers[i].find('td', {'data-col3 Ta(end) Pstart(20px) Miw(90px)'})
            print(cMarketTime.text)
            cChange = dataContainers[i].find('td', {'class':'data-col4 Ta(end) Pstart(20px)'})
            print(cChange.text)
            cPercentChng = dataContainers[i].find('span')
            print(cPercentChng.text)
            cVol = dataContainers[i].find('td', {'class':'data-col6 Ta(end) Pstart(20px)'})
            print(cVol.text)
            cAvgVol = dataContainers[i].find('td', {'class':'data-col7 Ta(end) Pstart(20px)'})
            print(cAvgVol.text)
            cMarketCap = dataContainers[i].find('td', {'class':'data-col8 Ta(end) Pstart(20px)'})
            print(cMarketCap.text)
            writer.writerow([timeStamp_string, cSymbol.text, cName.text, '$'+cLastPrice.text, cMarketTime.text, cChange.text, cPercentChng.text, cVol.text, cAvgVol.text, cMarketCap.text])

    with open('stock-scraper/data/allStoredStocks.csv', 'a', newline='', encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat('stock-scraper/data/allStoredStocks.csv').st_size == 0:
            writer.writerow(['time stamp', 'symbol', 'name', 'Last Price', 'Market Time', 'Change', '%Change', 'Volume', 'Avg Vol(3month)', 'Market Cap'])   #Fill in with the tags of the CSV#
        with open('stock-scraper/data/TrendingStocksToday.csv', 'r', newline='', encoding='UTF-8') as today_csv:
            reader = csv.reader(today_csv)
            next(reader)
            for row in reader:
                writer.writerow(row)
    mySched.enter(12, 1, scrape)


def clearCSV():
    f = open('stock-scraper/data/allStoredStocks.csv', 'w+')
    

def execChoice(choice):
    if choice == 'scrape':
        scrape()
    elif choice == 'clear':
        clearCSV()
    else:
        print('Some error aoccured and neither scrape() nor clearCSV() could be called.')

execChoice(usrChoice)
mySched.enter(12, 1, scrape)
mySched.run()

