#!/usr/bin/env python

import os
import time
import urllib2
import pytz
import pandas as pd
import pandas_datareader.data as web

from bs4 import BeautifulSoup
from datetime import datetime

WiKi_SITE = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
START_TIME = datetime.fromtimestamp(time.time() - 60 * 60 * 24 * 2)
END_TIME = datetime.today().utcnow()

def scrape_list(wiki_site):
    header = {'User-Agent': 'Mozilla/5.0'}
    request = urllib2.Request(wiki_site, headers=header)
    page = urllib2.urlopen(request)
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = list()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            ticker = str(col[0].string.strip())
            tickers.append(ticker)

    return tickers

def download_ohlc(company, start, end):
    print 'Downloading data from Yahoo for %s' % company
    data = web.DataReader(company, 'yahoo', start, end)
    if not os.path.isdir('data'):
        os.mkdir('data')

    data.to_csv('data/' + company + '.csv')

    print data.head()
    print 'Finished downloading data for %s' % company


def get_download_snp500():
    company_lists = scrape_list(WiKi_SITE)
    for company in company_lists:
        stock_ohlc = download_ohlc(company, START_TIME, END_TIME)

if __name__ == '__main__':
    get_download_snp500()
