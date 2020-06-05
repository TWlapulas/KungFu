# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:27:30 2019

@author: Steven
"""
from subprocess import Popen as subopen
from os import chdir as change_dir
from os import popen as osopen
from stem.control import Controller
from fake_useragent import UserAgent
from time import time
#----------------------------------------------------------------------
useragent = UserAgent()
hashcode_len = 61
#----------------------------------------------------------------------
class NotFoundError(Exception):
    pass
#----------------------------------------------------------------------
def myip(object):
    headers = {'User-Agent': useragent.random}
    res = object.get('http://icanhazip.com/', headers=headers)
    return res.text.strip()
#----------------------------------------------------------------------
def execute_tor(path='', tor_password='', control_port=9051, timeout=10):
    print('Starting Tor')
    start = time()
    p = subopen(path)
    while True:
        try:
            controller = tor_controller(tor_password, control_port)
            break
        except:
            if time()-start < timeout: continue
            p.kill()
            raise 
        
    while True:
        response = controller.get_info("status/bootstrap-phase")
        if response.find('SUMMARY="Done"'):
            print('Tor is working')
            return p, controller
        else:
            if time()-start < timeout: continue
            controller.close()    
            p.kill()
            raise TimeoutError('Tor open failed: '+response)
#----------------------------------------------------------------------
def tor_controller(tor_password='', control_port=9051):
    controller = Controller.from_port(port=control_port)
    controller.authenticate(password=tor_password)
    return controller
#----------------------------------------------------------------------
def hashcode_generator(path='TorFolderPath', password='TorPassword'):
    change_dir(path)
    with osopen(f"cmd /k tor --hash-password {password}") as p:
        cmd_info = p.read()
    for value in cmd_info.split():
        if all((value.startswith('16:'), len(value)==hashcode_len)):
            return value
    raise OSError(cmd_info)
#----------------------------------------------------------------------
def current_hashcode(torrc_path=''):
    with open(torrc_path, 'r') as torrc:
        lines = torrc.readlines()
    for line in lines:
        if any((line.startswith('HashedControlPassword'),
                line.startswith('#HashedControlPassword'))):
            return line.split()[1]
    raise NotFoundError("'HashedControlPassword' not found")
#----------------------------------------------------------------------
def replace_hashcode(torrc_path='', hashcode=''):
    current = current_hashcode(torrc_path)
    with open(torrc_path, 'r') as torrc:
        lines = torrc.readlines()
    i = 0
    while True:
        if any((lines[i].startswith('HashedControlPassword'),
                lines[i].startswith('#HashedControlPassword'))):
            lines[i] = lines[i].replace(current, hashcode)
            break
        i+=1
    with open(torrc_path, 'w') as torrc:
        torrc.writelines(lines)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
if __name__=='__main__': 
    #from time import sleep
    #from stem import Signal
    import requests

    session = requests.session()
    session.proxies = {
        'http' : 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    start = time()
    tor, _ = execute_tor(
        path = r'C:\Users\Steven\Desktop\Tor\tor.exe',
        tor_password = 'vpj358Kfpg'
    )
    end = time()
    print(f'time expend: {end-start:.3f} s')
    print('real ip: '+myip(requests))
    print('fake ip: '+myip(session))
    tor.kill()




