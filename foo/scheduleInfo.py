# coding=utf-8
from retrying import retry


@retry(stop_max_attempt_number=99)
def getscheduleinfo(mid, db, cursor):
    sql = "select * from schedule where mid = %d" % int(mid)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    re = results[0]
    return re


@retry(stop_max_attempt_number=99)
def insertscheduleinfo(mid, db, cursor, maxPage):
    # 删除原数据
    sql = "delete from schedule where mid = %d" % int(mid)
    # 插入现有数据
    sql2 = "insert into schedule (mid,page,size,max_page,complete)values(%d,1,1,%d,0)" % (int(mid), int(maxPage))
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


@retry(stop_max_attempt_number=99)
def updatescheduleinfo(mid, db, cursor, page, size):
    sql = "update schedule set page = %d , size = %d where mid = %d" % (int(page), int(size), int(mid))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


@retry(stop_max_attempt_number=99)
def completescheduleinfo(mid, db, cursor):
    sql = "update schedule set complete = 1 where mid = %d" % (int(mid))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
