# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:03:06 2019

@author: Steven
"""
import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
#------------------------------------------------------------------------------
useragent = UserAgent()
cookie_path = "D:/Python/KungFu/cookie.json"
#------------------------------------------------------------------------------
class TransitionError(Exception):
    pass
#------------------------------------------------------------------------------
def myip():
    headers = {'User-Agent': useragent.random}
    res = requests.get('http://icanhazip.com/', headers=headers)
    return res.text.strip()    
#------------------------------------------------------------------------------
def cookie_update(url):
    s = requests.session()
    s.get(url)
    cookies = s.cookies.get_dict()
    with open(cookie_path, 'w') as f:
        json.dump(cookies, f)
#------------------------------------------------------------------------------
def ip_check(ip, retryable=2):
    f = open(cookie_path, 'r')
    url = 'https://www.ez2o.com/App/Net/IP'
    headers = {'User-Agent': useragent.random}
    cookies = json.load(f)
    res = requests.get(url, headers=headers, cookies=cookies)
    try:
        soup = BeautifulSoup(res.text, 'lxml')
        input = soup.find('input')
        VerificationToken = input['value']
        data = {
                'QueryIP': ip,
                '__RequestVerificationToken': VerificationToken
        }
        res = requests.post(url, data=data, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.text, 'lxml')
        panel_body = soup.find('div', class_="panel-body")
        country = panel_body.find('span').text
        city = panel_body.find_all('tr', class_="active")[2].text
        f.close()
        return country, city
    except AttributeError:
        if retryable:
            f.close()
            cookie_update(url)
            return ip_check(ip, retryable-1)
        else:
            raise TransitionError('The server has no response')
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print(ip_check(myip()))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    