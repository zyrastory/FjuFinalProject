import pymysql

def Tocsv(num,a,b):
	mydb= pymysql.connect(host='localhost', port=3306, user='root', passwd='12345', db ='stock',charset='UTF8')
	cur = mydb.cursor()
	#cur.execute('SELECT open FROM fk WHERE date BETWEEN "2014-01-02 13:40:00" AND "2014-01-03 08:50:00"')

	#cur.execute('SELECT*FROM fk WHERE date BETWEEN "1998-07-22 00:00:00" AND "1999-07-22 00:00:00"')
	
	if num=="中石化":
		c='bbb'
	if num=="台泥":
		c='aaa'
	#if num=="中石化":
	#	c='aaa'
	#if num=="金指期":
	#	c='ccc'
	

	#cur.execute('SELECT*FROM '+c+ ' WHERE DateTime BETWEEN '+'"'+a+'"'+' AND '+'"'+b+'"')
	#cur.execute('SELECT*FROM '+c)
	cur.execute('SELECT*FROM  %s WHERE %s BETWEEN %s%s%s AND %s%s%s' %(c,"date",'"',a,'"','"',b,'"'))
	#print('SELECT*FROM '+c+ ' WHERE DateTime BETWEEN '+'"'+a+'"'+' AND '+'"'+b+'"')
	rows=cur.fetchall()

	x=""
	x+="Date Time,Open,High,Low,Close,Volume"+"\n"
	for rows in rows:
		for i in range(6):
			if i == 0:
				x+=(str(rows[i])+",")
			elif i == 5:
				x+=(" "+str(rows[i])+"\n")
			else:
				x+=(str(rows[i])+",")

	w = open("8-11.csv",'w')
	w.write(x)

	w.close