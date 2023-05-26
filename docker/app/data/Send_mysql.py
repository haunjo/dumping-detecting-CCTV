import pymysql
import pandas as pd
import os
import base64
from PIL import Image
from io import BytesIO

def send_mysql(cctv_id, filename, conn):
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = f"""insert into image(image_filename, cctv_no) values("{cctv_id}_{filename}",{cctv_id});"""
    print(sql)
    cur.execute(sql)
    conn.commit()


if __name__ == "__main__":
    conn = pymysql.connect(
        host='43.200.109.246',
        user='johaun', 
        password='8312', 
        db= 'SCV', 
        charset='utf8')
    
    try: 
        #send_mysql('6', "123", conn)
        sql = """select * from image;"""
        cur = conn.cursor(pymysql.cursors.DictCursor)
        #sql = f"""insert into image(image_filename, cctv_no) values({filename},{cctv_id});"""
        cur.execute(sql)
        a = cur.fetchall()
        print(a)
        conn.commit()
    finally:
        conn.close()

    


# conn.commit()
#conn.close()