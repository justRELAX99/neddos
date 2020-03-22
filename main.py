# -*- coding: utf-8 -*-
from datetime import datetime

from requests_html import *
from random import choice
from bs4 import BeautifulSoup
from selenium import webdriver
from math import ceil
import os
import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def auth_request(url,user_agent,proxy):
    session = HTMLSession()

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    proxies={
        'http':proxy
    }
    response = session.get(url, headers=headers,proxies=proxies,timeout=5)
    soup=BeautifulSoup(response.text,'lxml')
    post_url=soup.find(id='quick_login_form').get('action')
    post_elems=soup.find(id='quick_login_form').find_all('input')#парсим lg_h т.к. он меняется 
    for elem in post_elems:
        if(elem.get('name')=='lg_h'):
            lg_h=elem.get('value')
            break
    data=[
    ('act', 'login'), 
    ('role', 'al_frame'), 
    ('expire', ''), 
    ('_origin', 'https://vk.com'), 
    ('ip_h', 'e9d7291c1045299089'), 
    ('lg_h', lg_h),
    ('email', 'monstr541@yandex.ru'), 
    ('pass', 'bzr7quj991331AA')
    ]

    response = session.post(post_url, data=data,proxies=proxies,timeout=5)
    To_File(response.text,'html.txt')
    cookie=response.cookies
    session.close()
    return cookie


def auth_cookie_request(url,user_agent,proxy,cookie):
    session = HTMLSession()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    proxies={
        'http':proxy
    }
    # script = """
    # document.body.removeChild(document.getElementById('masthead'))"""
    response = session.get(url+'feed', headers=headers,proxies=proxies,cookies=cookie,timeout=5)
    #html=response.html
    #html.render(script=script)
    session.close()
    # soup=BeautifulSoup(response.text,'lxml')
    # name=soup.find(class_='top_profile_name').text
    #return name

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

def make_threads(data):
    urls=data[0]
    user_agents=data[1]
    proxies=data[2]
    cookies=data[3]
    with ThreadPoolExecutor(len(proxies)) as executor:
        names=list(executor.map(auth_cookie_request,urls,user_agents,proxies,cookies))
        return names

def test_cookie(url,user_agent,proxy):
    session = HTMLSession()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    proxies={
        'http':proxy
    }

    script = """
    document.getElementById('index_email').value = 'monstr541@yandex.ru'
    document.getElementById('index_pass').value = 'bzr7quj991331AA'
    document.getElementById('index_login_button').click()"""
    
    response=session.get(url, headers=headers,proxies=proxies,timeout=5)
    response.encoding='utf-8'
    html=response.html
    html.render(keep_page=True)
    return 123

def main():
    start=datetime.now()

    url='https://vk.com/'#тестовый
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'
    user_agents=open(name_user_agent).read().split('\n')
    proxies=open(name_proxy_file).read().split('\n')
    user_agent=choice(user_agents)
    
    #cookies=auth_request(url,user_agent,choice(proxies))
    cookies=[123]
    #auth_cookie_request(url,user_agent,choice(proxies),cookies)

    cookie2=test_cookie(url,user_agent,choice(proxies))
    #print(cookie2)
    # auth_cookie_request(url,user_agent,choice(proxies),cookie2)
    # cookie2=get_html_selenium(url,user_agent,choice(proxies))

    # print(cookie2)
    # get_html_selenium2(url,user_agent,choice(proxies),cookie2)

    cpu_count=os.cpu_count()

    parting_url=parting([url]*len(proxies),cpu_count)
    parting_user_agent=parting([user_agent]*len(proxies),cpu_count)
    parting_proxies=parting(proxies,cpu_count)
    parting_cookie=parting([cookies]*len(proxies),cpu_count)

    data=[]
    # for i in range(0,cpu_count):
    #     data.append([parting_url[i],parting_user_agent[i],parting_proxies[i],parting_cookie[i]])

    # with Pool(cpu_count) as p:
    #     names=list(p.map(make_threads,data))

    #print(len(names))
    end=datetime.now()
    total=end-start
    print(total)

if __name__ == "__main__":
    main()