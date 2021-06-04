import matplotlib.pyplot as plt

COUNT=[]
GA=[]
EGA=[]

with open("GA.txt","r") as file :
	for i in range(46):
		a=list(map(float,file.readline().split()))
		COUNT.append(a[0])
		GA.append(a[2])

with open("EGA.txt","r") as file :
	for i in range(46):
		a=list(map(float,file.readline().split()))
		EGA.append(a[2])


plt.plot(COUNT, GA, label = "GA")
plt.plot(COUNT, EGA, label = "EGA")


plt.xlabel('Number of Requests')
plt.ylabel('Time taken')
plt.title('Basic GA vs Enhanced GA')
plt.legend()
plt.show()
