import asyncio
from pyppeteer import launch

from itertools import repeat
from datetime import datetime
import time
from random import choice
from math import ceil
import os

async def get_browser(proxy=None,user_agent=None):
    return await launch({"headless": False})

async def get_cookies_peteer(url,user_agent,proxy,script_for_auth):
    browser = await get_browser()
    page = await browser.newPage()
    await page.goto(url)
    await page.evaluate(script_for_auth)
    await navPromise
    cookies=await page.cookies()
    await browser.close()
    return cookies

async def auth_with_cookies(url,user_agent,proxy,cookies,script_for_selenium):
    browser = await get_browser()
    page = await browser.newPage()
    await page.setCookie(*cookies)
    await page.goto(url)
    await page.evaluate(script_for_selenium)
    time.sleep(6)
    await browser.close()

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

async def get_proxy_by_numbers(name_proxy_file,numbers_proxy):
    all_proxies=open(name_proxy_file).read().split('\n')
    proxies=[]
    for i in numbers_proxy:
        proxies.append(all_proxies[i])
    return proxies

async def main(url,numbers_proxy,script_for_auth,script_for_selenium):
    start=datetime.now()
    
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'

    user_agents=open(name_user_agent).read().split('\n')

    if(len(numbers_proxy)!=0):
        proxies=await get_proxy_by_numbers(name_proxy_file,numbers_proxy)
    else:
        proxies=open(name_proxy_file).read().split('\n')

    user_agent=choice(user_agents)
    proxy=choice(proxies)

    cookies=await get_cookies_peteer(url,user_agent,proxy,script_for_auth)
    await auth_with_cookies(url,user_agent,proxy,cookies,script_for_selenium)
    end=datetime.now()
    total=end-start
    print(total)

if __name__ == "__main__":
    url='https://vk.com/'#тестовый
    numbers_proxy=[1,3,5]
    script_for_auth="""
    document.getElementById('index_email').value = 'monstr541@yandex.ru'
    document.getElementById('index_pass').value = 'bzr7quj991331AA'
    document.getElementById('index_login_button').click()"""
    script_for_selenium="""
    """

    asyncio.get_event_loop().run_until_complete(main(url,numbers_proxy,script_for_auth,script_for_selenium))