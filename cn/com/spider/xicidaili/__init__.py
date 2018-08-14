# encoding:utf-8
import sqlite3

import requests
from bs4 import BeautifulSoup

import sys                         #也就是在该文件代码开头添加这三行内容
reload(sys)
sys.setdefaultencoding('utf8')

# 请求url，获取网页数据
def _requestUrl(index):
    src_url = 'http://www.xicidaili.com/nt/'
    url = src_url + str(index)
    if index == 0:
        url = src_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    response = requests.get(url, headers=headers)
    return response.text


# 解析网页数据，获取ip和端口信息
def parseProxyIpList(content):
    list = []
    soup = BeautifulSoup(content, 'html.parser')
    ips = soup.findAll('tr')
    for x in range(1, len(ips)):
        tds = ips[x].findAll('td')
        ip_temp = 'http://' + tds[1].contents[0] + ':' + tds[2].contents[0]
        print('发现ip：%s' % ip_temp)
        list.append(ip_temp)
    return list

# 过滤有效的ip信息
def filterValidProxyIp(list):
    print('开始过滤可用ip 。。。')
    validList = []
    for ip in list:
        if validateIp(ip):
            print('%s 可用' % ip)
            validList.append(ip)
            save_db(ip)
        else:
            print('%s 无效' % ip)
    return validList

# 验证ip是否有效
def validateIp(proxy):
    proxy_temp = {"http": proxy}
    url = "http://ip.chinaz.com/getip.aspx"
    try:
        response = requests.get(url, proxies=proxy_temp, timeout=5)
        return True
    except Exception as e:
        return False


def save_db(ip):
    # print os.getcwd()  # 获得当前工作目录
    conn = sqlite3.connect('../../../../spider.db')
    c = conn.cursor()
    # Insert a row of data
    c.execute("INSERT INTO main.xicidaili(ip) VALUES ('"+ip+"')")
    # Save (commit) the changesprint os.getcwd()
    conn.commit()
    conn.close()

# 获取可用的代理ip列表
def getProxyIp():
    allProxys = []

    startPage = 1
    endPage = 30

    for index in range(startPage, endPage):
        print('查找第 %s 页的ip信息' % index)

        # 请求url，获取网页数据
        content = _requestUrl(index)
        # 解析网页数据，获取ip和端口信息
        list = parseProxyIpList(content)
        # 过滤有效的ip信息
        list = filterValidProxyIp(list)
        # 添加到有效列表中
        allProxys.append(list)

        print('第 %s 页的有效ip有以下：' % index)
        print(list)

    print('总共找到有效ip有以下：')
    print(allProxys)

    return allProxys


if __name__ == '__main__':
    print 'start'
    getProxyIp()