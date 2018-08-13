# # encoding:utf-8
import urllib
import urllib2
import cookielib
import re
import json
import requests
import sqlite3

#'''抓取网页文件内容，保存到内存@url 欲抓取文件 ，path+filename'''



def get_html(url):
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

        req = urllib2.Request(url,  headers=hdr)
        operate = opener.open(req)
        data = operate.read()
        return data
    except BaseException, e:
        print e
        return None


def get_id(url):
    print url
    data = get_html(url)
    #print data
    res_tr = r'data-menuid="(.*?)"'
    down_link = re.findall(res_tr, str(data), re.S | re.M)
    for id in down_link:
        print id
        post_index(id)


def post_index(id):
    url = 'https://msdn.itellyou.cn/Category/Index'
    formdata = {
        "id": id
    }
    response = post_http(url, formdata)
    print response
    for json in eval(response):
        print json['id']
        post_getLang(json['id'])


def post_getLang(id):
    url = 'https://msdn.itellyou.cn/Category/GetLang'
    formdata = {
        "id": id
    }
    response = post_http(url, formdata)
    result = json.loads(response)['result']
    print response
    for js in result:
        print js['id']
        post_getList(js['id'], id)


def post_getList(lang, id):
    url = 'https://msdn.itellyou.cn/Category/GetList'
    formdata = {
        "id": id,
        "lang": str(lang),
        "filter": bool(1)
    }
    response = post_http(url, formdata)
    print response

def post_http(url, formdata):
    # POST请求的目标URL
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '39',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.2.603077664.1525661152; UM_distinctid=163387db6391ab-07c7b034d2227e-3b700558-1fa400-163387db63ace3; ,CNZZDATA1605814=cnzz_eid%3D879266778-1525658695-null%26ntime%3D1525675410; _gid=GA1.2.1737191863.1534146588; Hm_lvt_8688ca4bc18cbc647c9c68fdaef6bc24=1534146588; Hm_lpvt_8688ca4bc18cbc647c9c68fdaef6bc24=1534146588',
        'Host': 'msdn.itellyou.cn',
        'Origin': 'https://msdn.itellyou.cn',
        'Referer': 'https://msdn.itellyou.cn/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = urllib.urlencode(formdata)
    request = urllib2.Request(url, data=data, headers=headers)
    #response = urllib2.urlopen(request)
    #return response.read()
    response = requests.post(url, data=data, headers=headers, timeout=120)
    return response.text

if __name__ == '__main__':
    get_id("https://msdn.itellyou.cn")