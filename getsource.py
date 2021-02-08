import pymysql
import requests
import threading

url = "https://static-data.eol.cn/www/2.0/school/102/info.json"

province = {
    "11":"北京市",
    "12":"天津市",
    "13":"河北省",
    "14":"山西省",
    "15":"内蒙古自治区",
    "21":"辽宁省",
    "22":"吉林省",
    "23":"黑龙江省",
    "31":"上海市",
    "32":"江苏省",
    "33":"浙江省",
    "34":"安徽省",
    "35":"福建省",
    "36":"江西省",
    "37":"山东省",
    "41":"河南省",
    "42":"湖北省",
    "43":"湖南省",
    "44":"广东省",
    "45":"广西壮族自治区",
    "46":"海南省",
    "50":"重庆市",
    "51":"四川省",
    "52":"贵州省",
    "53":"云南省",
    "54":"西藏自治区",
    "61":"陕西省",
    "62":"甘肃省",
    "63":"青海省",
    "64":"宁夏回族自治区",
    "65":"新疆维吾尔自治区",
    "71": "香港",
    '81': "澳门",
    '82': "台湾"
}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
}
mysql = {'host': 'localhost', 'port': 3306, 'user': 'root', 'passwd': 'sjh080815', 'db': 'college', 'charset': 'gbk'}
db = pymysql.connect(**mysql)
cursor = db.cursor()
counter_lock2 = threading.Lock()
def getcollege():

    sql = """SELECT id,name FROM college where id=1061"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print("Error: unable to fetch data")

def getgrade(row):
    url = "https://static-data.eol.cn/www/2.0/school/%s/info.json" % row[0]
    resopnse = requests.get(url=url, headers=headers)

    pro_type_min = dict(resopnse.json()['data']['pro_type_min'])

    print(row[1])


    for k,v in pro_type_min.items():

        for i in v:

            for type_k,type_v in i['type'].items():
                if type_k == '1':
                    classType = "理科"
                elif type_k == '2':
                    classType = "文科"
                elif type_k == '3':
                    classType = "不限"
                else:
                    classType = "其他"

                # print("%s年%s %s 最低分数线：%s" % (i['year'],province[k],classType,type_v))
                try:
                    sql = """ INSERT INTO grade(year, type, province, grade_min, college_id) VALUES ('%s','%s','%s',%d,%d)
                    """ % (i['year'],classType,province[k],int(type_v.split(".")[0]),row[0])
                except:
                    print("出错了")
                    continue
                try:
                        counter_lock2.acquire()
                        cursor.execute(sql)
                        db.commit()
                        counter_lock2.release()



                except:
                    db.rollback()
                    print(sql)
                    print("写入失败")


class getThread(threading.Thread):
    def __init__(self,row,num):
        threading.Thread.__init__(self)
        self.row = row
        self.num = num
    def run(self):
        with self.num:

            getgrade(self.row)

if __name__ == '__main__':
    result = getcollege()
    t = []
    threadingNum = threading.Semaphore(5)
    for row in result:
        t.append(getThread(row,threadingNum))
    for i in t:
        i.start()
    for i in t:
        i.join()
