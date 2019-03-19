# coding=utf-8
import json
import time
import urllib.request

import pymysql

from foo import listread

db = pymysql.connect(host='localhost', user='root', passwd='root', db='vtb', port=3306, charset='utf8')
cursor = db.cursor()

midList = []
durationList = [1, 2, 3, 4]  # 10分钟以下 10-30分钟 30-60分钟 60分钟以上
durationName = ['10分钟以下', '10-30分钟', '30-60分钟', '60分钟以上']
orderList = ['totalrank', 'click', 'pubdate', 'dm', 'stow']  # 综合排序 最多点击 最新发布 最多弹幕 最多收藏

keyword = 'VTuber'

for i in range(0, 4):
    for j in range(0, 1):
        print('正在进行  %s   %s' % (durationName[i], orderList[j]))
        duration = durationList[i]
        order = orderList[j]
        print('正在遍历')
        print('%d ' % 1, end="")
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=%s&order=%s&duration=%d&page=%s' % (
            keyword, order, int(duration), 1)
        obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        data = obj['data']
        maxPage = data['numPages']
        result = data['result']
        for item in result:
            midList.append(str(item['mid']))
        # 遍历
        if maxPage != 1:
            for nowPage in range(2, maxPage + 1):
                if nowPage % 10 == 0:
                    print('%d ' % nowPage)
                else:
                    print('%d ' % nowPage, end="")
                url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=%s&order=%s&duration=%d&page=%s' % (
                    keyword, order, int(duration), nowPage)
                obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
                result = obj['data']['result']
                for item in result:
                    midList.append(str(item['mid']))
                time.sleep(0.4)
        print("")
        # 去重
        oldList = listread.readlist('VTBList')
        listread.cleanlist('VTBList')
        midList += oldList
        midList.sort()
        midList = list(set(midList))
        listread.writelist('VTBList', midList)
