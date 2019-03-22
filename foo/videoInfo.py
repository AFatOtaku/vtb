# coding=utf-8
import json
import time
import urllib
import urllib.request

import pymysql
from retrying import retry

from foo import scheduleInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}


# 插入视屏信息
@retry(stop_max_attempt_number=99)
def getvideolist(mid, db, cursor):
    page = 1
    size = 1
    maxPage = 1
    data = None
    vlist = None
    re = scheduleInfo.getscheduleinfo(mid, db, cursor)
    # 如果没有数据
    if re is None:
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&pagesize=30&tid=0&page=%d&keyword=&order=pubdate' % (
            mid, page)
        obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        time.sleep(0.3)
        data = obj['data']
        vlist = data['vlist']
        maxPage = data['pages']
        insertvideoinfolist(vlist, 1, 1, db, cursor)
        scheduleInfo.insertscheduleinfo(mid, db, cursor, maxPage)
        page += 1
        size = 1
    else:
        # 有数据
        # 已经爬取完成
        if re[4] == 1:
            print(mid + "爬取已完成")
            return
        else:
            # 爬取到一半
            page = re[1]
            size = re[2]
            maxPage = re[3]
            print(mid + "继续爬取")
    # 循环到爬取整个页面
    for i in range(page, maxPage + 1):
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&pagesize=30&tid=0&page=%d&keyword=&order=pubdate' % (
            mid, i)
        obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        time.sleep(0.3)
        data = obj['data']
        vlist = data['vlist']
        insertvideoinfolist(vlist, i, size, db, cursor)
        size = 1
    scheduleInfo.completescheduleinfo(mid, db, cursor)


def insertvideoinfolist(vlist, page, size, db, cursor):
    print("正在爬取第%d页" % page)
    for i in range(size, len(vlist) + 1):
        item = vlist[i - 1]
        insertvideoinfo(item, page, i, db, cursor)


@retry(stop_max_attempt_number=99)
def insertvideoinfo(item, page, size, db, cursor):
    aid = item['aid']
    comment = item['comment']
    typeid = item['typeid']
    play = item['play']
    subtitle = item['subtitle']
    description = item['description']
    copyright = item['copyright']
    title = item['title']
    review = item['review']
    author = item['author']
    mid = item['mid']
    is_union_video = item['is_union_video']
    created = item['created']
    video_length = item['length']
    video_review = item['video_review']
    is_pay = item['is_pay']
    favorites = item['favorites']
    hide_click = item['hide_click']
    timeArray = time.localtime(created)
    otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    time1 = video_length.split(":", 1)
    sec = int(time1[0]) * 60 + int(time1[1])
    if play == '--':
        play = -1
    # 删除原数据
    # sql = r"delete from video_info where mid = %d" % int(aid)
    # 插入现有数据
    sql2 = r"insert ignore into video_info" \
           "(aid,video_comment,typeid,video_view,subtitle,description,copyright,title,reply," \
           "author,mid,is_union_video,created,video_length,video_review,is_pay,favorites,hide_click,duration)values(" \
           "%d,%d,%d,%d,'%s','%s','%s','%s',%d,'%s',%d,%d,'%s','%s',%d,%d,%d,%d,%s)" % (
               int(aid),
               int(comment),
               int(typeid),
               int(play),
               pymysql.escape_string(subtitle),
               pymysql.escape_string(description),
               pymysql.escape_string(copyright),
               pymysql.escape_string(title),
               review,
               pymysql.escape_string(author),
               int(mid),
               int(is_union_video),
               pymysql.escape_string(otherStyleTime),
               pymysql.escape_string(video_length),
               int(video_review),
               int(is_pay),
               int(favorites),
               int(hide_click),
               int(sec))
    try:
        # cursor.execute(sql)
        scheduleInfo.updatescheduleinfo(mid, db, cursor, page, size)
        cursor.execute(sql2)
        db.commit()
    except Exception as e:
        # print(sql)
        print(sql2)
        print(e)
        db.rollback()
    return
