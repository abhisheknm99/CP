import matplotlib.pyplot as plt

COUNT=[]
GA=[]
EGA=[]

with open("GA.txt","r") as file :
	for i in range(46):
		a=list(map(float,file.readline().split()))
		COUNT.append(a[0])
		GA.append(a[3])

comaparision_file_name ="DGA.txt"

with open(comaparision_file_name,"r") as file :
	for i in range(46):
		a=list(map(float,file.readline().split()))
		EGA.append(a[3])

fr=(sum(GA)/sum(EGA))-1
percent=100*fr
print("Percentage improvement :",percent)

