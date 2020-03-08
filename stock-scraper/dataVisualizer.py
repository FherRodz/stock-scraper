import plotly
import plotly.io as pio
import plotly.graph_objs as go
import plotly.plotly as py
import csv
import os
from plotly import __version__
print(__version__)
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot 

pio.renderers.default="browser"

name_price = dict()
with open('../stock-scraper/data/allStoredStocks.csv', 'r', newline='', encoding="UTF-8") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for line in reader:
        name_price[line[1]] = line[3][1:]

    for stock in name_price:
        print(stock,"     ",name_price[stock])


