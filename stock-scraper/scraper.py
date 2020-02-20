# Web Scraper script
#By Fher Rodriguez 

from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as req 
from urllib.request import FancyURLopener
import csv

class myOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11'    #Replace the string with your user agent

opener = myOpener()

myUrl = 'https://finance.yahoo.com/trending-tickers'    #Replace the string with the target web site URL

myClient = opener.open(myUrl)
mySoup = soup(myClient.read(), features = 'html.parser')
myClient.close()


#----------------------------------PARSE YOUR SOUP BELLOW----------------------------------#
dataContainers = mySoup.findAll('tr')
print('cont size: '+str(len(dataContainers)))
print(dataContainers[2].td.text)







# ------------Un-comment 4 lines bellow to save a copy of the web site HTML--------------#
soupHTML = open('soupHTML.html', 'w')
for line in mySoup.prettify(formatter = 'minimal'):
    soupHTML.write(str(line))
soupHTML.close()


# -------------Un-comment line below to save a CSV file with your scrapped data-------------#
with open('TrendingStocksToday.csv', 'w', newline="", encoding='UTF-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['symbol', 'name', 'Last Price', 'Market Time', 'Change', '%Change', 'Volume', 'Avg Vol(3month)', 'Market Cap'])   #Fill in with the tags of the CSV#
    reactid = 64
    for i in range(1,len(dataContainers)-1):
        if i == 1:
            reactid = 64
        else:
            reactid += 20
        print(i)
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
        cPercentChng = dataContainers[i].find('span', {'data-reactid':str(reactid)})
        print(cPercentChng.text)
        cVol = dataContainers[i].find('td', {'class':'data-col6 Ta(end) Pstart(20px)'})
        print(cVol.text)
        cAvgVol = dataContainers[i].find('td', {'class':'data-col7 Ta(end) Pstart(20px)'})
        print(cAvgVol.text)
        cMarketCap = dataContainers[i].find('td', {'class':'data-col8 Ta(end) Pstart(20px)'})
        print(cMarketCap.text)
        writer.writerow([cSymbol.text, cName.text, '$'+cLastPrice.text, cMarketTime.text, cChange.text, cPercentChng.text, cVol.text, cAvgVol.text, cMarketCap.text])


