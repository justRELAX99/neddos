from selenium import webdriver
import time
from bs4 import BeautifulSoup

def get_html(driver):
        driver.get('https://hidemy.name/ru/proxy-list/?maxtime=2000&type=h&anon=34')#http
        #driver.get('https://hidemy.name/ru/proxy-list/?maxtime=2000&type=s&anon=34#list')#https
        #driver.get('https://hidemy.name/ru/proxy-list/?maxtime=2000&type=hs&anon=34#list')#http and https
        time.sleep(6)
        requiredHtml =driver.page_source
        return requiredHtml
    
def get_proxy(html):
        soup=BeautifulSoup(html,'lxml')
        proxys=[]
        proxyTables=soup.find(class_='table_block').find('table').findAll('tr')
        for i in proxyTables:
            ip=i.find('td')
            port=ip.next_sibling
            proxys.append(ip.text+':'+port.text)
        proxys.pop(0)
        return proxys
    
def To_File_TXT(proxys):
        f=open('proxy_file.txt','w')
        for i in proxys:
            if(i!=proxys[-1]):
                f.write(i+'\n')
            else:
                f.write(i)
        f.close()



def get_ip(url,proxy):#
    proxies={
        'http':'http://'+proxy
        }
    print(proxies)
    try:
        response=requests.get(url,proxies=proxies,timeout=10).text
        soup=BeautifulSoup(response,'lxml')
        find_ip=soup.find(class_='ip')
        print(find_ip)
    except:
        print('ошибка подключения - ', proxy)

def main():
        driver=webdriver.Chrome('C:\\Users\\justRELAX\\Downloads\\chromedriver_win321\\chromedriver.exe')
        html=get_html(driver)
        proxys=get_proxy(html)
        To_File_TXT(proxys)
        driver.quit()
        
        # name_proxy_file='proxy_file.txt'
        # proxies=open(name_proxy_file).read().split('\n')
        # for proxy in proxies:
        #         get_ip('https://pr-cy.ru/browser-details/',proxy.strip())


if __name__=='__main__':
    main()
