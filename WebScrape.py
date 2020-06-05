# -*- coding: utf-8 -*-
import requests 
from re import compile
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from concurrent import futures
#------------------------------------------------------------------------------
useragent = UserAgent()
headers = {'user-agent': useragent.random}
#------------------------------------------------------------------------------
def url_encode(key):
    url = 'https://www.urlencoder.org/'
    data = {
        'input': key,
        'charset': 'UTF-8',
        'separator': 'LF'
    }
    res = requests.post(url, data=data)
    soup = BeautifulSoup(res.text, features='lxml')
    return soup.find_all('textarea')[1].text.strip()
#------------------------------------------------------------------------------
def proxy_list(version='http'):
    if version=='http':
        URL = 'https://free-proxy-list.net/'
    elif version=='https':
        URL = 'https://www.sslproxies.org/'
    else:  #socks
        URL = 'https://www.socks-proxy.net/'
    res = requests.get(URL, headers=headers)    
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', id="proxylisttable")
    ip_and_port = table.find_all('td', text=compile('^\d.*\d$'))
    it = iter(ip_and_port)
    ProxyList = []
    while True:
        try:
            ip = next(it).text.strip()
            port = next(it).text.strip()
            ProxyList.append(ip+':'+port)
        except StopIteration:
            break
    return ProxyList
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def multiurl(urls, connections, fn, **kwargs):  # fn 的第一個參數必須是 url
    result = []
    with futures.ThreadPoolExecutor(max_workers=connections) as executor:
        future_to_url = (executor.submit(fn, url, **kwargs) for url in urls)
        for future in futures.as_completed(future_to_url):
            try:
                result.append(future.result())
            except:
                raise
    return result
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__=='__main__':
    for p in proxy_list():
        print(p)










