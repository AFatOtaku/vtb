# coding=utf-8
import pymysql

from foo import listread, videoInfo, userInfo

db = pymysql.connect(host='localhost', user='root', passwd='root', db='vtb', port=3306, charset='utf8')
cursor = db.cursor()
userList = listread.readlist('VTBList')
userList.sort(key=None, reverse=False)
for user in userList:
    print(user)
    re = userInfo.insertUserInfoWithCheck(user, db, cursor)
    videoInfo.getvideolist(user, db, cursor)
db.close()
