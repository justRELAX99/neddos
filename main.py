from datetime import datetime
from memory_profiler import memory_usage

from requests_html import *
from random import choice
from bs4 import BeautifulSoup

from concurrent.futures import ProcessPoolExecutor
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
    soup=BeautifulSoup(response.text,'lxml')
    name=soup.find(class_='top_profile_name').text
    session.close()
    return name

def print123(url,user_agent,proxy,cookie):
    return('url-',url,';user_agent-',user_agent,';proxy-',proxy,';cookie-',cookie)

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

def main():
    start=datetime.now()

    url='https://vk.com/'#тестовый
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'
    user_agents=open(name_user_agent).read().split('\n')
    proxies=open(name_proxy_file).read().split('\n')
    user_agent=choice(user_agents)
    cookie=auth_request(url,user_agent,choice(proxies))
    
    with ThreadPoolExecutor(len(proxies)) as executor:
        names=list(executor.map(auth_cookie_request,repeat(url),repeat(user_agent),proxies,repeat(cookie)))

    print(names)

    end=datetime.now()
    print(memory_usage(),'---end')
    total=end-start
    print(total)

if __name__ == "__main__":
    main()