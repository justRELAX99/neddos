import requests
from selenium import webdriver
from requests_html import HTMLSession
from requests_html import requests
import time
from memory_profiler import memory_usage
import io

from random import choice
from multiprocessing import Pool

def get_html(url,user_agent,proxy):
    header={
        'User-Agent':user_agent
        }
    proxies={
        'http':proxy
        }
    response = requests.get(url,headers=header,proxies=proxies)

    return response.text

def get_request_html(url,user_agent,proxy):
    header={
        'User-Agent':user_agent
        }
    proxies={
        'http':proxy
        }

    script = """
    document.body.removeChild(document.getElementById('masthead'))"""
    session = HTMLSession()
    response=session.request('get',url,headers=header,proxies=proxies).html
    response.render(script=script)
    session.close()
    return response.html

def get_html_selenium(url):
        options=webdriver.ChromeOptions()
        options.add_argument("--headless")
        script = """
        document.body.removeChild(document.getElementById('masthead'))"""  
        driver=webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
        driver.execute_script(script)
        html =driver.page_source
        driver.quit()
        return html

def To_File_TXT(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()


def get_status_code(url,proxy,user_agent):
    header={
        'User-Agent':user_agent
        }

    proxies={
        'http':proxy
        }

    try:
        response=requests.get(url,headers=header,proxies=proxies,timeout=10)
        print(response.content)
        return response.status_code
    except:
        return (proxy,'-Ошибка подключения')

def main():
    url='https://python-scripts.com/'#тестовый
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'

    user_agents=open(name_user_agent).read().split('\n')
    proxies=open(name_proxy_file).read().split('\n')

    user_agent=choice(user_agents)
    proxy=choice(proxies)
    To_File_TXT (get_html(url,user_agent,proxy),'html.html')
    #To_File_TXT(get_html_selenium(url),'html2.txt')
    #To_File_TXT(get_request_html(url,user_agent,proxy),'html3.html')
    # for proxy in proxies:
    #     user_agent=choice(user_agents)
    #     status_code=get_status_code(url,proxy,user_agent)
    #     if(status_code!=200):
    #         print(status_code)
    #     break
    print(memory_usage())

if __name__ == "__main__":
    main()