import requests
from random import choice
from multiprocessing import Pool

def get_status_code(url,proxy,user_agent):
    header={
        'User-Agent':user_agent
        }

    proxies={
        'http':proxy
        }
    try:
        response=requests.get(url,headers=header,proxies=proxies,timeout=3)
        return response.status_code
    except:
        print('0')


def send_request(proxy):
    url='https://python-scripts.com/'#тестовый
    name_user_agent='user_agent.txt'
    user_agents=open(name_user_agent).read().split('\n')
    user_agent=choice(user_agents)
    if(get_status_code(url,proxy,user_agent)==False):
        print(get_status_code(url,proxy,user_agent))


def main():
    name_proxy_file='proxy_file.txt'
    proxies=open(name_proxy_file).read().split('\n')

    for i in range(0,len(proxies)-1):
        with Pool(len(proxies)-5) as p:
            p.map(send_request,proxies)
        print(i)


if __name__ == "__main__":
    main()