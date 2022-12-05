# -*- coding: utf-8 -*-

import urllib.request as req
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import requests

# in case of time out，refresh the page
def requestDemo(url):
    # update the headers
    headers = {'User-Agent': '..'}
    trytimes = 5  # times of retry
    for i in range(trytimes):
        try:
            response = requests.get(url, headers=headers, proxies=None, timeout=5)
            html = response.text
            # status code being 200 means accessing the page successfully. 
            if response.status_code == 200:
                return html
        except:
            print(f'requests failed {i} time')

# area: district name of Shanghai （string）
# page: the page number starts from，the defalt is from the fisrt page (number）
def get_inf(area, page=1):
    # get the total number of pages
    host = "https://sh.lianjia.com/ershoufang/"
    tmpSubSoup = BeautifulSoup(req.urlopen(host + area), "lxml")
    total = eval(tmpSubSoup.select('div[class="page-box house-lst-page-box"]')[0].get("page-data"))['totalPage']
    # turn pages from one to the last
    for i in range(page, total + 1):
        print("page" + str(i))
        if i == 1:  # the website of the first page
            pagehtml = requestDemo(host + area)
        else:  # website of the other page
            pagehtml = requestDemo(host + area + "/pg" + str(i) + "/")
        pageSoup = BeautifulSoup(pagehtml, "lxml")
        # get the list of all the houses in the current page 
        url_list = pageSoup.find("ul", {"class": "sellListContent"}).findAll("div", {"class": "title"})
        print(url_list)
        print(len(url_list))
        # iterate the housing list
        for l in url_list:
            de_url = l.find('a')['href']
            print(de_url)
            with open(area + '.csv', 'a', newline='') as f:  # create csv
                writer = csv.writer(f)
                try:
                    html = requestDemo(de_url)  # website of one house
                    soup = BeautifulSoup(html, "lxml")  # parse the data
                    name = soup.find("h1", {"class": "main"}).get_text()  # house name
                    price = soup.find("span", {"class": "unitPriceValue"}).get_text()  # house pice
                    communityName = soup.find("div", {"class": "communityName"}).find("a", {"class": "info"}).get_text()  # community name
                    build_year = soup.find("div", {"class": "area"}).find("div", {"class": "subInfo"}).get_text()  # build year
                    datas = soup.find("div", {"class": "base"}).findAll("li")  # other information
                    lst = []
                    for data in datas:
                        lst.append(data.get_text())
                    # wirte the file
                    # ' House Name', 'House Price', 'Community Name', 'Build Year', 'House Type', 'Floor', 'Area', 'Structure', 'Using Area', 'Architecture Type', 'Direction', 'Architecture Structure', 'Decoration Condition','Elevator to Door Ratio ', 'Elevator'
                    # '房屋名称', '房屋均价', '小区名称', '年份', '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况','梯户比例', '装备电梯'
                    writer.writerow([name, price, communityName, build_year, lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8], lst[9], lst[10], i])
                    # time staying on the web
                    time.sleep(16 + random.randint(0, 9))
                except Exception as e:
                    print(str(e))


# Shanghai as the example
# list of all the Shanghai district
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

    # iterate all the district of the city
    for j in areaList:
        area = j
        print(area)
        get_inf(area)
    print("finished")
