import pymysql

db = pymysql.connect(host='localhost', user='root', db='perfumes', password='zoqtmxhsqlqjs', charset='utf8', port=3306)
curs = db.cursor()

ret = []

sql = "select * from test;"
curs.execute(sql)

rows = curs.fetchall()
for p in rows:
    temp = {'id':p[0],'perfume_name':p[1],'brand':p[2],'gender':p[3]}
    ret.append(temp)

print(ret)

db.commit()
db.close()