# coding=utf-8
import datetime
import time

import pymysql
from retrying import retry


@retry(stop_max_attempt_number=99)
def cutTag(item, db, cursor, nowSum, totalSum, time_start):
    try:
        time_end = time.time()
        print('time cost:', time_end - time_start, 's now time:', datetime.datetime.fromtimestamp(time_end)),
        print("  第%d/%d个 目前进度%.4f%% 视频ID: %d" % (nowSum, totalSum, nowSum * 100 / totalSum, item[0]))
        sql = "insert video_tag(aid,tid,tname) " \
              "(select a.aid,substring_index(substring_index(a.tag_id,',',b.help_topic_id+1),',',-1) ,substring_index(substring_index(a.tag_name,',',b.help_topic_id+1),',',-1) " \
              "from video_info a join mysql.help_topic b on b.help_topic_id < (length(a.tag_id) - length(replace(a.tag_id,',','')))" \
              " where a.aid = %d order by a.aid)" % item[0]
        sql2 = "update video_info set tag_cut_flag = 1 where aid = %d" % item[0]
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()
    except Exception as e:
        print(e)
        time.sleep(1)
        db.rollback()


@retry(stop_max_attempt_number=99)
def cutTagList():
    db = pymysql.connect(host='localhost', user='root', passwd='root', db='vtb', port=3306, charset='utf8')
    cursor = db.cursor()
    searchSql1 = "select count(1) from video_info where tag_cut_flag = 1"
    cursor.execute(searchSql1)
    nowSum = cursor.fetchall()[0]
    sum = nowSum[0]
    searchSql2 = "select count(1) from video_info"
    cursor.execute(searchSql2)
    totalSum = cursor.fetchall()[0]
    time_start = time.time()
    while 1:
        searchSql = "select aid from video_info where tag_cut_flag is null or tag_cut_flag = 0 order by aid limit 50"
        cursor.execute(searchSql)
        results = cursor.fetchall()
        if len(results) == 0:
            break
        for item in results:
            sum += 1
            cutTag(item, db, cursor, sum, totalSum[0], time_start)

cutTagList()