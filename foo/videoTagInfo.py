# coding=utf-8
import datetime
import json
import time
import urllib.request

import pymysql
from retrying import retry

from foo import videoDetailInfo


@retry(stop_max_attempt_number=99)
def getTagInfo(item, db, cursor, nowSum, totalSum, time_start):
    try:
        tagIdList = ""
        tagNameList = ""
        url = 'https://api.bilibili.com/x/tag/archive/tags?aid=%s' % item[0]
        obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        time.sleep(0.3)
        if "data" in obj.keys():
            data = obj['data']
            for tagItem in data:
                tagIdList += str(tagItem['tag_id']) + ','
                tagNameList += tagItem['tag_name'] + ','
        time_end = time.time()
        print('time cost: %.3f s now time:  %s ' % (time_end - time_start,datetime.datetime.fromtimestamp(time_end)))
        print("  第%d/%d个  目前进度%.4f%% 视频ID: %d tag:%s" % (nowSum, totalSum, nowSum*100 / totalSum, item[0], tagNameList))
        sql = r"update video_info set tag_id = '%s',tag_name = '%s',tag_flag = 1 where aid = %d" % (
        pymysql.escape_string(tagIdList), pymysql.escape_string(tagNameList), item[0])

        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        time.sleep(1)
        db.rollback()


@retry(stop_max_attempt_number=99)
def getTagInfoList():
    db = pymysql.connect(host='localhost', user='root', passwd='root', db='vtb', port=3306, charset='utf8')
    cursor = db.cursor()
    sum = 0
    time_start = time.time()
    searchSql1 = "select count(1) from video_info where tag_flag = 1"
    cursor.execute(searchSql1)
    nowSum = cursor.fetchall()[0]
    sum = nowSum[0]
    searchSql2 = "select count(1) from video_info"
    cursor.execute(searchSql2)
    totalSum = cursor.fetchall()[0]
    while 1:
        searchSql = "select aid from video_info where tag_flag is null or tag_flag = 0 order by aid limit 50"
        cursor.execute(searchSql)
        results = cursor.fetchall()
        if len(results) == 0:
            db.close()
            videoDetailInfo.getDetailInfoList()
            break
        for item in results:
            sum += 1
            getTagInfo(item, db, cursor, sum, totalSum[0], time_start)


getTagInfoList()
