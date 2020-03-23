from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from memory_profiler import memory_usage

from random import choice
from multiprocessing import Pool


def get_cookies_selenium(url,user_agent,proxy):
    options=webdriver.ChromeOptions()
    options.add_argument('--proxy-server-%s'%proxy)
    options.add_argument('user-agent='+user_agent)
    options.add_argument("--headless")
    script = """
    document.getElementById('index_email').value = 'monstr541@yandex.ru'
    document.getElementById('index_pass').value = 'bzr7quj991331AA'
    document.getElementById('index_login_button').click()"""
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
        driver.execute_script(script)
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

def auth_with_cookies_selenium(url,user_agent,proxy,cookies):
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
        print('Performed')
        driver.quit()
        return 1


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
    proxy=choice(proxies)
    
    cookies=get_cookies_selenium(url,user_agent,proxy)
    if(cookies!=0):
        auth_with_cookies_selenium(url,user_agent,proxy,cookies)

    print(memory_usage())
    end=datetime.now()
    total=end-start
    print(total)

if __name__ == "__main__":
    main()