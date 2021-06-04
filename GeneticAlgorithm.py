# Imports
from random import choices,randint,random
import timeit
from tkinter import ttk
from tkinter import *

# Global variables
number_of_requests = 30
Requests =[]
reuslt=[]
used_resources=[0,0,0]
time_taken =0

# ############################################################################################
# # Input Request Generation
# ############################################################################################
# # Ratio of resources for each slice type
# types =[[2,2,3] ,[1,2,3],[4,2,1]]
# #Length of request file.
# length = 100
# with open("requests.txt","w") as file :
# 	for i in range(length):
# 		r =randint(1,10)
# 		t=randint(0,2)
# 		output = [str(x * r) for x in types[t]]
# 		output.append(str(choices([50,100,150,200,250,300,350,400,450,500],k=1)[0]))
# 		file.write(" ".join(output))
# 		file.write("\n")


# Input
with open("requests.txt","r") as file:
	for i in range(number_of_requests):
		a=list(map(int,file.readline().split()))
		Requests.append(a)


#Algorithm Parameters  
gene_length = number_of_requests
population_size = max(50,number_of_requests * 5)
number_of_parents = 4
mutation_bits = 1
mutation_probability = 0.3
generation_limit = 500
stagnation_limit = 30
drule1 = 1
drule2 = 1

# Available resources (A, B, C)
ramax=100
rbmax=100
rcmax=100

# Dispacthing Rule 1
def dr_1():
	temp=[]
	for i in range(len(Requests)):
		temp.extend([Requests[i][0],Requests[i][1],Requests[i][2]])
	res_ratio = min(ramax,rbmax,rcmax)//max(temp)
	weight_factor = res_ratio / gene_length
	return [0.5+weight_factor,0.5-weight_factor]

# Generate Genome based on weights from dispaching rule
def random_gene (length):
	if drule1==0:
			return choices([0,1],k=length,weights=[0.5,0.5])
	else:
			return choices([0,1],k=length,weights=dr_1())

# Generate population
def generate_population (length):
	population =[]
	for i in range(length):
		population.append(random_gene(gene_length))
	population=dr_2(population)
	correction_factor=[0]*gene_length
	correction_factor[0]=1
	population.append(correction_factor)
	return population

# Dispacthing Rule 2
def dr_2(Population):
	temp=[0]*gene_length
	for i in range(len(Population)):
		for j in range(gene_length):
			temp[j] =temp[j] | Population[i][j]
	if sum(temp)>0:
		Population.append(temp)
	return Population

	 
# Fitness function
def fitness_function (gene):
	ra=0
	rb=0
	rc=0
	revenue=0

	for i in range(len(gene)):
		if gene[i] == 1:
			ra += Requests[i][0]
			rb += Requests[i][1]
			rc += Requests[i][2]
			revenue += Requests[i][3]
	if (ra > ramax) or (rb > rbmax) or (rc > rcmax):
		return 0
	
	return revenue


# Select genes from population for next generation.
def selection_function(Population) :
	return choices(Population, weights =[fitness_function(x) for x in Population], k = number_of_parents)


# Crossover function to create next generation
def crossover_function (Parents,splitpoint):
	Children = []
	for i in range(number_of_parents-1):
		Children.append(Parents[i][0:splitpoint] + Parents[i+1][splitpoint:])
	Children.append(Parents[number_of_parents-1][0:splitpoint] + Parents[0][splitpoint:])
	return Children

# Diploid crossover with 2 split points
def diploid_crossover(Parents):
	splitpoint1 = randint(1,gene_length -1)
	splitpoint2 = randint(1,gene_length -1)
	Children = []
	Clones=Parents.copy()
	Children.extend(crossover_function(Parents,splitpoint1))
	Children.extend(crossover_function(Clones,splitpoint2))
	return Children


# Mutation 
def mutation_function (gene):
	for i in range(mutation_bits):
		index = randint(0,gene_length-1)
		prob = random()
		if prob > mutation_probability:
			gene[index] = 1 - gene[index] 
	return gene

# Evolution 
def evolution(Population,evolution_type):
	Population = sorted(Population ,key=fitness_function,reverse=True)
	prev=fitness_function(Population[0])
	stagnation = 0
	generation = 0
	Children=[]

	for i in range(generation_limit):
		
		if fitness_function(Population[0]) == prev:
			stagnation+=1
		else:
			stagnation =0

		prev=fitness_function(Population[0])
		if stagnation == stagnation_limit:
			return (Population[0],fitness_function(Population[0]),generation)

		NextGeneration = []
		NextGeneration.extend(Population[:population_size//2])

		while len(NextGeneration)<= population_size:
			Parents = selection_function(Population)
			if evolution_type == 1:
				splitpoint = randint(1,gene_length -1)
				Children = crossover_function(Parents,splitpoint)
			elif evolution_type == 2:
				Children =diploid_crossover(Parents)

			for i in Children:
				NextGeneration.append(mutation_function(i))
		Population = NextGeneration[0:population_size]
		generation+=1
		Population = sorted(Population ,key=fitness_function,reverse=True)
	return (Population[0],fitness_function(Population[0]),generation)



# Function to compute time taken to reach solution (factor of 5 for comparision with C++)
def TimeGA(evolution_type):
	global time_taken
	global result
	start = timeit.default_timer()
	Population = generate_population(population_size)
	result = evolution(Population,evolution_type)
	stop = timeit.default_timer()
	print("Slicing Strategy ",result[0])
	print("Maximum revenue value" ,[result[1]])
	print("Generation number",result[2])
	time_taken = (stop-start)/5
	print("Time Taken",time_taken)


# compute resources utilized
def calculate_used_resources():
	global used_resources
	for i in range(len(Requests)):
		if result[0][i]==1:
			used_resources[0]+=Requests[i][0]
			used_resources[1]+=Requests[i][1]
			used_resources[2]+=Requests[i][2]


# Run diploid multiparent evolution with dispatching rules
drule1 = 1
drule2 = 2
number_of_parents =4
print("Diploid evolution")
TimeGA(2)
calculate_used_resources()

##################################################################
# GUI
##################################################################

# GUI Attributes
accepted_color="green"
rejected_color="#C25B56"
outline_color="black"
line_width=2
min_limit=10
max_limit=30
inter_resource_gap =20
row_gap=20
rccol="#525564"
rbcol="#74828F"
racol="#96C0CE"


# Single block of request
def create_request_block(canvas,beginx,beginy,decision,width=20,ra=min_limit,rb=min_limit,rc=min_limit,gap=inter_resource_gap):
	weight1=min(max(min_limit,ra),max_limit)
	weight2=min(max(min_limit,rb),max_limit)
	weight3=min(max(min_limit,rc),max_limit)
	col1=""

	if decision ==1:
		col1=accepted_color
	elif decision ==0:
		col1=rejected_color

	startx = beginx
	starty = beginy+gap

	ax1=startx
	bx1=startx
	cx1=startx

	ax2=ax1+width
	bx2=bx1+width
	cx2=cx1+width

	ay1=starty
	ay2=ay1+weight1

	by1=ay2
	by2=by1+weight2

	cy1=by2
	cy2=cy1+weight3

	canvas.create_text((ax1+ax2)//2,ay1-gap,text=str(decision),fill=col1,font=('Times', '24', 'bold'))
	canvas.create_rectangle(ax1,ay1,ax2,ay2,fill=racol,outline=outline_color,width=line_width)
	canvas.create_rectangle(bx1,by1,bx2,by2,fill=rbcol,outline=outline_color,width=line_width)
	canvas.create_rectangle(cx1,cy1,cx2,cy2,fill=rccol,outline=outline_color,width=line_width)


# Generates the chart of requests with multiple request blocks
def generate_chart(canvas):
	startx=50
	starty=50
	gap = 80
	count=0
	col=0

	for i in range(len(Requests)):
		create_request_block(canvas,startx,starty,result[0][i],ra=Requests[i][0],rb=Requests[i][1],rc=Requests[i][2])
		startx=startx+gap
		count+=1
		if count==10:
			starty+=(3*max_limit+inter_resource_gap+row_gap)
			startx=50
			count=0
			col+=1
		if col==3:
			break


#Simulator
def runsimulator():
	#Main Window---------------------------------------------------------
	root = Tk()
	root.title("Slice Simulator")
	root.geometry("1920x1080+-10+0")
	# root.attributes('-fullscreen',True)

	# Seperator object----------------------------------------------------
	separator = ttk.Separator(root, orient='vertical')
	separator.place(relx=0.65, rely=0, relwidth=0.35, relheight=0.7)
	separator = ttk.Separator(root, orient='horizontal')
	separator.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

	rightCanvas=Canvas(root, bg ="silver")
	rightCanvas.place(relx=0.652, rely=0, relwidth=0.348, relheight=0.698)

	bottomCanvas=Canvas(root, bg ="silver")
	bottomCanvas.place(relx=0, rely=0.704, relwidth=1, relheight=0.296)
	root.configure(background='white')


	canvas=Canvas(root,bg="white")
	canvas.place(relx=0, rely=0, relwidth=0.65, relheight=0.7)


	rightCanvas.create_text(270,75,fill="darkblue",font="Times 28 italic bold",text="Resource Pool")

	generate_chart(canvas)

	#Resource Table
	xpos=7
	ypos=150

	avlRes=used_resources
	color1=[racol,rbcol,rccol]

	for z in range(3):
		count=0
		st=xpos
		for x in range(10):
			for y in range(10):
				if count>avlRes[z]:
					fill_color="white"
				else:
					fill_color=color1[z]
				cell=rightCanvas.create_rectangle(10, 10, 24, 24, outline="black", fill=fill_color)
				rightCanvas.move(cell,xpos,ypos)
				xpos+=16
				count+=1
			ypos+=16
			end=xpos+10
			xpos=st
		xpos=end
		ypos=150


	rightCanvas.create_text(100,340,font="Times 16",text="Resource A")
	rightCanvas.create_text(270,340,font="Times 16",text="Resource A")
	rightCanvas.create_text(438,340,font="Times 16",text="Resource A")


	#Bottom Canvas: Info tab ----------------------------------------------------------------------------------------

	console = Button(root, text="Console Output",font="Times 14")
	console.place(relx=.85, rely=0.75, relwidth=0.1, relheight=0.07)

	stat = Button(root, text="Stats & Graph",  font="Times 14")
	stat.place(relx=.85, rely=0.85, relwidth=0.1, relheight=0.07)

	bottomCanvas.create_text(70,30,font="Times 16 italic bold",text="Execution Details:",anchor=W)

	bottomCanvas.create_text(70,60,font="Times 14",text="Execution Time: "+str(time_taken),anchor=W)
	bottomCanvas.create_text(70,80,font="Times 14",text="Number of Generations: "+str(result[2]),anchor=W)
	bottomCanvas.create_text(70,100,font="Times 14",text="Maximum revenue:"+str(result[1]),anchor=W)
	bottomCanvas.create_text(70,120,font="Times 14",text="Decision Vector: "+str(result[0]),anchor=W)

	mainloop()

runsimulator()
