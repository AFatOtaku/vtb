# coding=utf-8
import json
import time
import urllib.request

import pymysql
from retrying import retry


def getuserinfo(mid, db, cursor):
    sql = "select * from user_info where mid = %d" % int(mid)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    re = results[0]
    return re


def insertUserInfoWithCheck(uid, db, cursor):
    re = getuserinfo(uid, db, cursor)
    if re is not None:
        return None
    else:
        insertUserInfo(uid, db, cursor)
        return 1


# 插入BILIBILI会员基础信息
@retry(stop_max_attempt_number=99)
def insertUserInfo(uid, db, cursor):
    # 基础信息
    url = 'https://api.bilibili.com/x/space/acc/info?mid=' + uid
    # 关注 被关注
    url2 = 'https://api.bilibili.com/x/relation/stat?vmid=' + uid
    # 视频 相册 音乐 等投稿数
    url3 = 'https://api.bilibili.com/x/space/navnum?mid=' + uid
    # 总播放
    url4 = 'http://api.bilibili.com/x/space/upstat?mid=' + uid

    print("正在爬取:" + uid)
    print("开始爬取信息")
    obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    time.sleep(0.3)
    obj2 = json.loads(urllib.request.urlopen(url2).read().decode('utf-8'))
    time.sleep(0.3)
    obj3 = json.loads(urllib.request.urlopen(url3).read().decode('utf-8'))
    time.sleep(0.3)
    data = obj['data']
    data2 = obj2['data']
    data3 = obj3['data']
    mid = data['mid']
    name = data['name']
    sex = data['sex']
    face = data['face']
    sign = data['sign']
    level = data['level']
    birthday = data['birthday']
    coins = data['coins']
    rank = data['rank']
    following = data2['following']
    follower = data2['follower']
    album = data3['album']
    article = data3['article']
    audio = data3['audio']
    bangumi = data3['bangumi']
    cinema = data3['cinema']
    video = data3['video']
    # 删除原数据
    sql = r"delete from user_info where mid = %d" % mid
    # 插入现有数据
    sql2 = r"insert into user_info" \
           "(mid,name,sex,face,sign,level,birthday,coins,user_rank,following," \
           "follower,album,article,audio,bangumi,cinema,video)values(" \
           "%d,'%s','%s','%s','%s',%d,'%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % (
               int(mid),
               pymysql.escape_string(name),
               pymysql.escape_string(sex),
               pymysql.escape_string(face),
               pymysql.escape_string(sign),
               int(level),
               pymysql.escape_string(birthday),
               int(coins),
               int(rank),
               int(following),
               int(follower),
               int(album),
               int(article),
               int(audio),
               int(bangumi),
               int(cinema),
               int(video))
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()
    except Exception as e:
        print(sql2)
        print(e)
        db.rollback()
    return
