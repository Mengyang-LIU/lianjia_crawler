# -*- coding: utf-8 -*-

import urllib.request as req
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import requests


# 防止页面time out，如果time out后尝试刷新页面
def requestDemo(url):
    # 根据更新本地headers
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    trytimes = 5  # 重试的次数
    for i in range(trytimes):
        try:
            response = requests.get(url, headers=headers, proxies=None, timeout=5)
            html = response.text
            # 状态码为200即为访问页面成功 返回所需html结束循环
            if response.status_code == 200:
                return html
        except:
            print(f'requests failed {i} time')


# area 上海区域（字符串）
# page 从该页开始，默认为从第一页开始（数字）
def get_inf(area, page=1):
    # 获得总页数total
    host = "https://sh.lianjia.com/ershoufang/"
    tmpSubSoup = BeautifulSoup(req.urlopen(host + area), "lxml")
    total = eval(tmpSubSoup.select('div[class="page-box house-lst-page-box"]')[0].get("page-data"))['totalPage']
    # 从1到最后页翻页
    for i in range(page, total + 1):
        print("page" + str(i))
        if i == 1:  # 第一页网址
            pagehtml = requestDemo(host + area)
        else:  # 其他页网址
            pagehtml = requestDemo(host + area + "/pg" + str(i) + "/")
        pageSoup = BeautifulSoup(pagehtml, "lxml")
        # 获得当前页面的所有房屋列表
        url_list = pageSoup.find("ul", {"class": "sellListContent"}).findAll("div", {"class": "title"})
        print(url_list)
        print(len(url_list))
        # 历遍房屋列表
        for l in url_list:
            de_url = l.find('a')['href']
            print(de_url)
            with open(area + '.csv', 'a', newline='') as f:  # 创建csv
                writer = csv.writer(f)
                try:
                    html = requestDemo(de_url)  # 访问房屋网址,timeout设置超时的时间
                    soup = BeautifulSoup(html, "lxml")  # 解析网址
                    name = soup.find("h1", {"class": "main"}).get_text()  # 获得房屋名称
                    price = soup.find("span", {"class": "unitPriceValue"}).get_text()  # 获得房屋均价
                    communityName = soup.find("div", {"class": "communityName"}).find("a", {"class": "info"}).get_text()  # 获得小区名称
                    build_year = soup.find("div", {"class": "area"}).find("div", {"class": "subInfo"}).get_text()  # 获得年份
                    datas = soup.find("div", {"class": "base"}).findAll("li")  # 获得其他信息
                    lst = []
                    for data in datas:
                        lst.append(data.get_text())
                    # 写入文件
                    # '房屋名称', '房屋均价', '小区名称', '年份', '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况','梯户比例', '装备电梯'
                    writer.writerow([name, price, communityName, build_year, lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8], lst[9], lst[10], i])
                    # 模拟人访问在网页停留时间
                    time.sleep(16 + random.randint(0, 9))
                except Exception as e:
                    print(str(e))


# 以上海市为例
# 上海所有区域列表
# 'pudong', 'minhang', 'baoshan', 'xuhui', 'putuo',
# 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu',
# 'jingan', 'hongkou', 'qingpu', 'fengxian', 'jinshan',
# 'chongming', 'shanghaizhoubian'

if __name__ == '__main__':
    tmpMainSoup = BeautifulSoup(req.urlopen("https://sh.lianjia.com/ershoufang/"), "lxml")
    a = tmpMainSoup.find("div", {"data-role": "ershoufang"}).findAll("a")
    areaList = []
    for n in a:
        areaName = n.get('title')
        if areaName == None:
            continue
        else:
            areaLink = n.get('href')
            found = re.search('/ershoufang/(.+?)/', areaLink).group(1)
            print(found)
            areaList.append(found)
    print(areaList)

    # 历遍每一个区域
    for j in areaList:
        area = j
        print(area)
        get_inf(area)
    print("finished")
