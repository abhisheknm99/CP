from random import randint,choices

types =[[2,2,3] ,[1,2,3],[4,2,1]]

length = 100


with open("requests.txt","w") as file :
	for i in range(length):
		r =randint(1,10)
		t=randint(0,2)

		output = [str(x * r) for x in types[t]]
		output.append(str(choices([50,100,150,200,250,300,350,400,450,500],k=1)[0]))


		file.write(" ".join(output))
		file.write("\n")

