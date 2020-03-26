import asyncio
from pyppeteer import launch

from itertools import repeat
from datetime import datetime
import time
from random import choice
from math import ceil
import os

async def get_browser(proxy=''):
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    if(proxy!=''):
        #return await launch(args=['--proxy-server=http='+proxy,'user-agent='+user_agent],headless=False)
        return await launch(args=['--proxy-server=http='+proxy],headless=False)
    else:return await launch({'headless': False})

async def get_cookies_peteer(url,proxy,script_for_auth):
    try:
        browser = await get_browser(proxy)
    except:
        print('Не удалось создать браузер')
        await browser.close()
        return 0

    try:
        page = await browser.newPage()
    except:
        print('Не удалось создать страницу')
        await browser.close()
        return 0
    
    try:
        await page.goto(url)
    except:
        print('Не удалось загрузить url')
        await browser.close()
        return 0
    try:
        await page.evaluate(script_for_auth)
    except:
        print('Не удалось выполнить скрипт')
        await browser.close()
        return 0
    try:
        await page.waitForSelector('#feed_add_list_icon')#Добавляем id,который будет ожидать на странице
        cookies=await page.cookies()
        await browser.close()
        return cookies
    except:
        print('Не удалось найти элемент')
        await browser.close()
        return 0

async def auth_with_cookies(url,proxy,cookies,script_for_selenium):
    try:
        browser = await get_browser(proxy)
    except:
        print('Не удалось создать браузер')
        await browser.close()
        return 0
    try:
        page = await browser.newPage()
    except:
        print('Не удалось создать страницу')
        await browser.close()
        return 0
    try:
        await page.setCookie(*cookies)
    except:
        print('Не удалось добавить cookies')
        await page.close()
        await browser.close()
        return 0
    try:
        await page.goto(url)
    except:
        print('Не удалось загрузить url')
        await browser.close()
        return 0
    
    try:
        await page.evaluate(script_for_selenium)
    except:
        print('Не удалось выполнить скрипт')
        await browser.close()
        return 0
    try:
        await page.waitForSelector('#feed_add_list_icon')#Добавляем id,который будет ожидать на странице
        await browser.close()
        return 1
    except:
        print('Не удалось найти элемент')
        await browser.close()
        return 0

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if(len(numbers_proxy)!=0):
        proxies=get_proxy_by_numbers(name_proxy_file,numbers_proxy)
    else:
        proxies=open(name_proxy_file).read().split('\n')
    
    proxy=choice(proxies)
    cookies=asyncio.get_event_loop().run_until_complete (get_cookies_peteer(url,proxy,script_for_auth))
    
    async def extract_all(url,proxies,cookies,script_for_selenium):
        tasks = []
        for proxy in proxies:
            task=asyncio.ensure_future(auth_with_cookies(url,proxy,cookies,script_for_selenium))
            tasks.append(task)
        print(tasks)
        responses = await asyncio.gather(*tasks)
        return responses

    if(cookies!=0):
        future = asyncio.ensure_future(extract_all(url,proxies,cookies,script_for_selenium))
        responses=asyncio.get_event_loop().run_until_complete(future)
        loop.close()
        
    print(responses)
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