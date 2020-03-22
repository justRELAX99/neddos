import requests
from selenium import webdriver
from requests_html import HTMLSession
from requests_html import requests
import time
from datetime import datetime
from memory_profiler import memory_usage
import io

from random import choice
from multiprocessing import Pool


def get_html_selenium3(url,user_agent,proxy):
    options=webdriver.ChromeOptions()
    options.add_argument('--proxy-server-%s'%proxy)
    options.add_experimental_option('w3c', False)
    #options.add_argument("--headless")
    script = """
    document.getElementById('index_email').value = 'monstr541@yandex.ru'
    document.getElementById('index_pass').value = 'bzr7quj991331AA'
    document.getElementById('index_login_button').click()"""
    driver=webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)
    driver.execute_script(script)
    cookies =driver.get_cookies()
    driver.quit()
    return cookies

def get_html_selenium2(url,user_agent,proxy,cookies):
    options=webdriver.ChromeOptions()
    options.add_argument('--proxy-server-%s'%proxy)
    options.add_experimental_option('w3c', False)
    #options.add_argument("--headless")
    driver=webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)

    for cookie in cookies:
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)

    print(driver.get_cookies())
    time.sleep(6)
    driver.quit()


def get_html_selenium(url,user_agent,proxy):
        options=webdriver.ChromeOptions()
        options.add_argument('--proxy-server-%s'%proxy)
        #options.add_argument("--headless")
        script = """
        document.body.removeChild(document.getElementById('masthead'))"""  
        driver=webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
        driver.execute_script(script)
        html =driver.page_source
        driver.quit()
        return html

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

def main():
    start=datetime.now()
    url='https://python-scripts.com/'#тестовый
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'

    user_agents=open(name_user_agent).read().split('\n')
    proxies=open(name_proxy_file).read().split('\n')

    user_agent=choice(user_agents)
    proxy=choice(proxies)
    for proxy in proxies:
        user_agent=choice(user_agents)
        html=get_html_selenium(url,user_agent,proxy)
        To_File(html,'html.html')
        break
    print(memory_usage())
    end=datetime.now()
    total=end-start
    print(total)

if __name__ == "__main__":
    main()