# encoding:utf-8
import cookielib
import re
import sqlite3
import string

import sys                         #也就是在该文件代码开头添加这三行内容
import urllib
import urllib2

import requests

reload(sys)
sys.setdefaultencoding('utf8')


def get_db():
    allProxys = []
    # print os.getcwd()  # 获得当前工作目录
    conn = sqlite3.connect('../../../../spider.db')
    c = conn.cursor()
    # Insert a row of data
    cursor = c.execute("select * from main.xicidaili")
    # Save (commit) the changesprint os.getcwd()
    for row in cursor:
        # print "IP = ", row[0]
        allProxys.append(row[0])
    conn.close()
    return allProxys



def post_http(url, formdata, proxy):
    # POST请求的目标URL
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "198",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "ll=118281; bid=1dMNnSwDlMo; _vwo_uuid_v2=D7FE6CDD39D902CA7B46086FBD2207874|4c744e210e056abdf505c5cfdfcd0587; __utma=30149280.967020144.1528010120.1528010120.1534172068.2; __utmc=30149280; __utmz=30149280.1534172068.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.967020144.1528010120; _gid=GA1.2.182509446.1534172366; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.12502; ap=1; douban-profile-remind=1; __utmb = 30149280.25.9.1534172454858; as=https://www.douban.com/notification/",
        "Host": "accounts.douban.com",
        "Origin": "https://www.douban.com",
        "Referer": "https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/people/125020023/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 68.0.3440.106 Mobile Safari / 537.36"
    }
    data = urllib.urlencode(formdata)
    print data
    #request = urllib2.Request(url, data=data, headers=headers)
    #response = urllib2.urlopen(request)
    #return response.read()
    proxy_temp = {"http": proxy, "https": proxy}
    print proxy_temp

    response = requests.post(url, data=data, headers=headers, timeout=120, proxies=proxy_temp)
    #session = requests.sessions()
    print response.text
    return response.text



def login(proxy):
    url='https://accounts.douban.com/login'
    formdata = {
        "source": "None",
        "form_email": "15817161961",
        "redir":"https://www.douban.com",
        "form_password": "1227241900zx",
        "captcha-solution": "store", # 验证码
        "captcha-id": "ulK875xnsOpIhEzDeBvZ1E7u:en", # 验证码图片id
        "remember": "on"
    }
    try:
        response = post_http(url, formdata, proxy)
        res_tr = r'<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"/>'
    except Exception as e:
        print e.message
    #img_link = re.findall(res_tr, str(response), re.S | re.M)[0]
    #print img_link


if __name__ == '__main__':
    list = get_db()
    for index in list:
        print string.replace(str(index), 'http://','')
        login(string.replace(str(index), 'http://',''))

