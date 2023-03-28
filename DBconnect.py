import pymysql
import pandas as pd
import os
import base64
from PIL import Image
from io import BytesIO
conn = pymysql.connect(
    host='127.0.0.1',
    user='root', 
    password='8312', 
    db= 'SCV', 
    charset='utf8')

cur = conn.cursor(pymysql.cursors.DictCursor)

buffer = BytesIO()

work_dir = 'data'
dir_list = os.listdir(f'{work_dir}/images')
print(dir_list)
for images in dir_list[1:]:
    file_list = os.listdir(f'{work_dir}/images/{images}')
    for image in file_list:
        print(image)
        sql = f"""insert into image (cctv_id, filename) values (1, '{image}')"""
        cur.execute(sql)
        conn.commit()
conn.close()