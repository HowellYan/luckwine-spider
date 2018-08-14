# # encoding:utf-8
import string
import urllib
import urllib2
import cookielib
import re
import json
from time import sleep

import requests
import sqlite3

import tesserocr
import os
# import textract
from PIL import Image
import pytesseract
import sys                         #也就是在该文件代码开头添加这三行内容
reload(sys)
sys.setdefaultencoding('utf8')


session = requests.session()

def post_http(url, formdata):
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
    response = session.post(url, data=data, headers=headers, timeout=120)
    print response.text
    return response.text

#創建文件目录，并返回该目录
def mkdir(path):
    # 去除左右两边的空格
    path = path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def save_file(path, file_name, data):
    if data == None:
        return
    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


# '''抓取网页文件内容，保存到内存@url 欲抓取文件 ，path+filename'''
def get_file(url):
    try:
        cj = cookielib.LWPCookieJar()
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url, headers=hdr)
        operate = opener.open(req)
        data = operate.read()
        return data
    except BaseException, e:
        print e
        return None

def login():
    url='https://www.douban.com/accounts/login'
    formdata = {
        "source": "None",
        "form_email": "15817161961",
        "redir":"https://www.douban.com",
        "form_password": "1227241900zx",
        "captcha-solution": "brother", # 验证码
        "captcha-id": "LaWfXy8orhmAw5XhjVtF2hQs:en", # 验证码图片id
        "remember": "on"
    }
    return post_http(url, formdata)
    res_tr = r'<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"/>'
    img_link = re.findall(res_tr, str(response), re.S | re.M)[0]
    print img_link

    #response = get_file('https://www.douban.com')
    #print response
    #res_tr = r'<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"'
    #img_link = re.findall(res_tr, str(response), re.S | re.M)[0]
    #print img_link
    #save_file("../../../../img", "captcha.jpg", get_file(img_link))
    #print tesserocr.file_to_text("/home/howell/PycharmProjects/luckwine-spider/img/captcha.jpg")
    #print Image.open('/home/howell/PycharmProjects/luckwine-spider/img/captcha.jpg')
    #print pytesseract.image_to_string(Image.open('/home/howell/PycharmProjects/luckwine-spider/img/captcha.jpg'))


def index():
    url = 'https://www.douban.com/accounts/'
    print session
    response = session.get(url)
    print response.text



if __name__ == '__main__':
    login()
    index()