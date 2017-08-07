import pymysql

def Tocsv():
	mydb= pymysql.connect(host='localhost', port=3306, user='root', passwd='12345', db ='mysql_test',charset='UTF8')
	cur = mydb.cursor()
#cur.execute('SELECT open FROM fk2 WHERE date BETWEEN "2014-01-02 13:40:00" AND "2014-01-03 08:50:00"')

#cur.execute('SELECT*FROM fk WHERE date BETWEEN "1998-07-22 00:00:00" AND "1999-07-22 00:00:00"')
	cur.execute('SELECT*FROM fk2 ')
	rows=cur.fetchall()

	x=""
	x+="Date,Open,High,Low,Close,Volume"+"\n"
	for rows in rows:
		for i in range(6):
			if i == 0:
				x+=(str(rows[i])+",")
			elif i == 5:
				x+=(" "+str(rows[i])+"\n")
			else:
				x+=(str(rows[i])+",")

	w = open("8-7.csv",'w')
	w.write(x)

	w.close