from datetime import datetime
from requests_html import *
from memory_profiler import memory_usage
from random import choice
from multiprocessing import Pool


def auth_request(url,user_agent):
    session = HTMLSession()
    
    header={
        'User-Agent':user_agent
        }

    data={
        'login':'monstr541@yandex.ru',
        'password':'bzr7quj9913'
    }
    response=session.post(url,headers=header,data=data)
    print(response.cookies)
    response=session.get('https://vk.com/feed')
    html=response.html
    html.render()
    To_File(html.html,'html4.txt')
    print('---------------------------------')
    print(response.cookies)
    print('---------------------------------')
    session.close()

def get_request_html(url,user_agent,proxy,session):
    header={
        'User-Agent':user_agent
        }
    proxies={
        'http':proxy
        }

    script = """
    document.body.removeChild(document.getElementById('masthead'))"""
    response=session.request('get',url,headers=header,proxies=proxies,timeout=5)
    html=response.html
    html.render(script=script)
    return html.html

def To_File(html,name):
        f=open(name,'w', encoding='utf-8')
        f.write(html)
        f.close()

def main():
    start=datetime.now()

    url='https://auth.mail.ru/cgi-bin/auth?from=splash'#тестовый
    name_user_agent='user_agent.txt'
    name_proxy_file='proxy_file.txt'
    responses=[]
    user_agents=open(name_user_agent).read().split('\n')
    proxies=open(name_proxy_file).read().split('\n')
    
    # session = HTMLSession()
    # for proxy in proxies:
    #     user_agent=choice(user_agents)
    #     response=get_request_html(url,user_agent,proxy,session)
    #     responses.append(response)
    # else:
    #     session.close()
    #print(responses)
    user_agent=choice(user_agents)
    auth_request(url,user_agent)
    end=datetime.now()
    print(memory_usage(),'---end')
    total=end-start
    print(total)

if __name__ == "__main__":
    main()