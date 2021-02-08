import requests
from selenium import webdriver
import json
import pymysql
mysql = {'host': 'localhost', 'port': 3306, 'user': 'root', 'passwd': 'sjh080815', 'db': 'college', 'charset': 'gbk'}
db = pymysql.connect(**mysql)
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
}
for i in range(1,96):
    url = "https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page=%d&province_id=&request_type=1&school_type=&signsafe=&size=30&sort=view_total&type=&uri=apidata/api/gk/school/lists" % i

    response = requests.post(url=url,headers=headers)
    datas = response.json()['data']['item']
    for data in datas:
        sql = """INSERT INTO college(id, name, level_name, nature_name, province_name, city_name, type_name, address)
                 VALUES (%d,'%s','%s','%s','%s','%s','%s','%s')""" % \
              (data['school_id'],data['name'],data['level_name'],
               data['nature_name'],data['province_name'],data['city_name'],
               data['type_name'], data['address'])
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("写入失败 %s" % data['name'])
