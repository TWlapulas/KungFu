# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:09:54 2019

@author: Steven
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def driver_ip(driver):
    try:
        driver.get('http://ip.filefab.com/index.php')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ipd')))
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        return soup.find('h1', id='ipd').text.split(':')[1].strip()
    except:
        raise 

