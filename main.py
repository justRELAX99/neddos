from selenium import webdriver
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Pool

from itertools import repeat
from datetime import datetime
import time
from random import choice
from math import ceil
import os

def get_cookies_selenium(url,user_agent,proxy,script_for_auth):
    options=webdriver.ChromeOptions()
    options.add_argument('--proxy-server-%s'%proxy)
    options.add_argument('user-agent='+user_agent)
    #options.add_argument("--headless")
    driver=webdriver.Chrome('chromedriver.exe', options=options)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    try:
        driver.get(url)
    except:
        print('The request failed')
        driver.quit()
        return 0
    try:
        driver.execute_script(script_for_auth)
    except:
        print('The script failed')
        driver.quit()
        return 0
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ui_rmenu_news_list")))
    except:
        print('Element not found')
        driver.quit()
        return 0
    finally:
        cookies =driver.get_cookies()
        driver.quit()
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry']*1000)
        return cookies

def test_proxy_auth(url,user_agent,proxy):
    options=webdriver.ChromeOptions()
    options.add_argument('--proxy-server-%s'%proxy)
    options.add_argument('user-agent='+user_agent)
    #options.add_argument("--headless")
    driver=webdriver.Chrome('chromedriver.exe', options=options)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    driver.get(url)
    print(proxy)
    print(user_agent)
    time.sleep(10)
    driver.quit()

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

def get_proxy_by_numbers(name_proxy_file,numbers_proxy):
    all_proxies=open(name_proxy_file).read().split('\n')
    proxies=[]
    for i in numbers_proxy:
        proxies.append(all_proxies[i])
    return proxies

def main(url,numbers_proxy,script_for_auth,script_for_selenium):
    start=datetime.now()
    
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'

    user_agents=open(name_user_agent).read().split('\n')

    if(len(numbers_proxy)!=0):
        proxies=get_proxy_by_numbers(name_proxy_file,numbers_proxy)
    else:
        proxies=open(name_proxy_file).read().split('\n')

    user_agent=choice(user_agents)
    proxy=choice(proxies)

    cookies=get_cookies_selenium(url,user_agent,proxy,script_for_auth)
    # if(cookies!=0):
    #     auth_with_cookies_selenium(url,user_agent,proxy,cookies)

    #test_proxy_auth('https://2ip.ru/',user_agent,proxy)
    
    #cookies=get_cookies_selenium(url,user_agent,proxy)
    
    with ThreadPoolExecutor(len(proxies)) as executor:

        def scrape(proxy, *, loop):
            nonlocal url
            nonlocal user_agent
            nonlocal cookies
            nonlocal script_for_selenium
            loop.run_in_executor(executor,auth_with_cookies_selenium, url,user_agent,proxy,cookies,script_for_selenium)

        def auth_with_cookies_selenium(url,user_agent,proxy,cookies,script_for_selenium):
            options=webdriver.ChromeOptions()
            options.add_argument('--proxy-server-%s'%proxy)
            options.add_argument('user-agent='+user_agent)
            options.add_argument("--headless")
            driver=webdriver.Chrome('chromedriver.exe', options=options)
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
            try:
                driver.get(url)
            except:
                driver.quit()
                print('The request failed')
                return 0
            
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ui_rmenu_news_list")))
            except:
                print('Element not found')
                driver.quit()
                return 0
            finally:
                try:
                    driver.execute_script(script_for_selenium)
                    print('Performed')
                    driver.quit()
                    return 1
                except:
                    print('The script failed')
                    driver.quit()
                    return 0

        loop = asyncio.get_event_loop()
        for proxy in proxies:
            scrape(proxy, loop=loop)

        answer=loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))


    pprint.pprint(answer)
    end=datetime.now()
    total=end-start
    print(total)

if __name__ == "__main__":
    url='https://vk.com/'#тестовый
    numbers_proxy=[]
    script_for_auth="""
    document.getElementById('index_email').value = 'monstr541@yandex.ru'
    document.getElementById('index_pass').value = 'bzr7quj991331AA'
    document.getElementById('index_login_button').click()"""
    script_for_selenium="""
    """
    main(url,numbers_proxy,script_for_auth,script_for_selenium)