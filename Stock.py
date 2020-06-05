# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:43:01 2019

@author: User
"""
import requests
from urllib3 import disable_warnings
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from re import compile
#------------------------------------------------------------------------------
useragent = UserAgent()
#------------------------------------------------------------------------------
def current_price(code, retry=3):
    price_url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{code}.tw&json=1&delay=0'
    disable_warnings()
    while True:
        try:
            price_dic = requests.get(
                    price_url, 
                    headers={'user-agent': useragent.random}, 
                    timeout=1, 
                    verify=False
                    ).json()
            break
        except:
            if not retry: raise
            retry-=1
    msgArray = price_dic['msgArray'][0]
    return msgArray['z']
#------------------------------------------------------------------------------
def code_list():
    url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    try:
        res = requests.get(
                url, 
                headers={'user-agent': useragent.random}, 
                timeout=10
                )
        soup = BeautifulSoup(res.text, 'lxml')
        code = compile('^\d')
        trs = soup.find_all('tr')
        container = []
        for tr in trs[2:]:
            text = tr.find('td').text
            if code.match(text):
                container.append(text[:4])
            else:
                return container
    except:
        raise
#------------------------------------------------------------------------------
def address(code):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t05st03'
    data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'co_id': code
    }
    res = requests.post(url, data, headers={'User-Agent': useragent.random})
    soup = BeautifulSoup(res.text, 'lxml')
    tds = soup.find_all('td')
    return tds[6].text
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__=='__main__':
    print(address(2330))















    
