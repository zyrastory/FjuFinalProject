import os

f = open("1101.csv",'r', encoding = 'utf8')
k = open("fk.txt",'w', encoding = 'utf8')

line=f.readline()
u=[]


while line:
	#print(line)
	if line[6]=="/":
		a=line[:5]+"0"+line[5:]
		u.append(a)
	else:
		u.append(line)
	line = f.readline()

#print(u)
str1 = "".join(u)
k.write(str1)

f.close()
k.close()

x = open("fk.txt",'r', encoding = 'utf8')
y = open("final.txt",'w', encoding = 'utf8')

line=x.readline()
u2=[]

while line:
	#print(line)
	if line[9]==",":
		b=line[:8]+"0"+line[8:]
		u2.append(b)
	else:
		u2.append(line)
	line = x.readline()

str2 = "".join(u2)
y.write(str2)

x.close()
y.close()

print("finsh!!!"*3)
os.system("del fk.txt")