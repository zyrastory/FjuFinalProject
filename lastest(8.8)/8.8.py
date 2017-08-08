import pymysql

mydb= pymysql.connect(host='localhost', port=3306, user='root', passwd='12345', db ='mysql_test',charset='UTF8')
cur = mydb.cursor()



a='1day'
b="1998-07-30 00:00:00"
c="1998-10-02 00:00:00"
#cur.execute('SELECT*FROM '+a+ ' WHERE DateTime BETWEEN "1998-07-30 00:00:00" AND "1998-10-02 00:00:00"')
#print('SELECT*FROM '+a+ ' WHERE DateTime BETWEEN "1998-07-30 00:00:00" AND "1998-10-02 00:00:00"')
cur.execute('SELECT*FROM '+a+ ' WHERE DateTime BETWEEN '+'"'+b+'"'+' AND '+'"'+c+'"')
rows=cur.fetchall()

for rows in rows:
	print(rows)