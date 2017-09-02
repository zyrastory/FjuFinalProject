import os

listA = []
for dirPath, dirNames, fileNames in os.walk \
("C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User"):
    fileNames = [ fi for fi in fileNames if  fi.endswith(".md") ]
    for f in fileNames:
        listA.append(f.replace(".md",""))
print(listA)
print(len(listA))
#print(listA[3][1])


for i in range(len(listA)):
     if listA[i].find("O") != -1:
        a = listA[i]
print(a)