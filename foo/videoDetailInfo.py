# coding=utf-8
import datetime
import json
import time
import urllib.request

import pymysql
from retrying import retry


@retry(stop_max_attempt_number=99)
def getDetailInfo(item, db, cursor, nowSum, totalSum, time_start):
    try:
        url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % item[0]
        obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        time.sleep(0.3)
        if "data" in obj.keys():
            data = obj['data']
            stat = data['stat']
            dimension = data['dimension']
            videos = data['videos']
            copyright = data['copyright']
            pic = data['pic']
            if "attribute" in data.keys():
                attribute = data['attribute']
            else:
                attribute = -1
            width = dimension['width']
            height = dimension['height']
            coin = stat['coin']
            share = stat['share']
            now_rank = stat['now_rank']
            his_rank = stat['his_rank']
            like = stat['like']
            dislike = stat['dislike']
            time_end = time.time()
            nowTime = time_end - time_start
            print('time cost: %d h %d m %.3f s now time:  %s ' % (
                nowTime / 3600, (nowTime / 60) % 60, nowTime % 60, datetime.datetime.fromtimestamp(time_end)))
            print("  第%d/%d个 目前进度%.4f%% 视频ID: %d" % (nowSum, totalSum, nowSum * 100 / totalSum, item[0]))
            sql = r"update video_info set videos = %d, copyright = %d, " \
                  r"pic = '%s', attribute = %d, width = %d, " \
                  r"height = %d, coin = %d, video_share = %d, now_rank = %d, his_rank = %d, " \
                  r"video_like = %d, dislike = %d, info_flag =1 where aid = %d" % (
                      videos,
                      copyright,
                      pymysql.escape_string(pic),
                      attribute,
                      width,
                      height,
                      coin,
                      share,
                      now_rank,
                      his_rank,
                      like,
                      dislike,
                      item[0]
                  )
        else:
            time_end = time.time()
            print('time cost:', time_end - time_start, 's now time:', datetime.datetime.fromtimestamp(time_end)),
            print("  第%d/%d个 目前进度%.4f%%  视频ID: %d  权限不足" % (nowSum, totalSum, nowSum * 100 / totalSum, item[0]))
            sql = "update video_info set info_flag = 2 where aid = %d" % item[0]
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        print(sql)
        time.sleep(5)
        db.rollback()


@retry(stop_max_attempt_number=99)
def getDetailInfoList():
    db = pymysql.connect(host='localhost', user='root', passwd='root', db='vtb', port=3306, charset='utf8')
    cursor = db.cursor()
    searchSql1 = "select count(1) from video_info where info_flag = 1"
    cursor.execute(searchSql1)
    nowSum = cursor.fetchall()[0]
    sum = nowSum[0]
    searchSql2 = "select count(1) from video_info"
    cursor.execute(searchSql2)
    totalSum = cursor.fetchall()[0]
    time_start = time.time()
    while 1:
        searchSql = "select aid from video_info where info_flag is null or info_flag = 0 order by aid limit 50"
        cursor.execute(searchSql)
        results = cursor.fetchall()
        if len(results) == 0:
            break
        for item in results:
            sum += 1
            getDetailInfo(item, db, cursor, sum, totalSum[0], time_start)
