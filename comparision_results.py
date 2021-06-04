from random import choices,randint,random
import timeit

# lists to store times
itr=[]
GA=[]
MPGA=[]
DGA=[]
DRGA=[]
EGA=[]

# # Genration and fitness
# GEN=[]
# FIT=[]

# Read requests
Requests =[]
with open("requests.txt","r") as file:
	for i in range(100):
		a=list(map(int,file.readline().split()))
		Requests.append(a)


# Loop for requests from 5 to 51
for aaa in range(5,51):
	number_of_requests = aaa
	reuslt=[]



##########################################
#Algorithm
##########################################

	#Algorithm Parameters
	gene_length = number_of_requests
	population_size = max(50,number_of_requests * 5)
	number_of_parents = 2
	mutation_bits = 1
	mutation_probability = 0.3
	generation_limit = 500
	stagnation_limit = 50
	drule1=0
	drule2=0

	# Resources  (A, B, C)
	ramax=100
	rbmax=100
	rcmax=100

	def dr_1():
		temp=[]
		for i in range(number_of_requests):
			temp.extend([Requests[i][0],Requests[i][1],Requests[i][2]])
		res_ratio = min(ramax,rbmax,rcmax)//max(temp)
		weight_factor = res_ratio / gene_length
		return [0.5-weight_factor,0.5+weight_factor]

	# Generate Random gene
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
		if drule2 == 1:
				population=dr_2(population)
		correction_factor=[0]*gene_length
		correction_factor[0]=1
		population.append(correction_factor)
		return population

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

	def evolution(Population,evolution_type):
		Population = sorted(Population ,key=fitness_function,reverse=True)
		prev=fitness_function(Population[0])
		stagnation = 0
		generation = 0
		Children=[]

		for i in range(generation_limit):
			Population = sorted(Population ,key=fitness_function,reverse=True)
			
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
			# GEN.append(generation)
			# FIT.append(fitness_function(Population[0]))
		return (Population[0],fitness_function(Population[0]),generation)


	def TimeGA(evolution_type,rarr):
		global result
		start = timeit.default_timer()
		Population = generate_population(population_size)
		result = evolution(Population,evolution_type)
		stop = timeit.default_timer()
		# print("Slicing Strategy ",result[0])
		# print("Maximum revenue value" ,[result[1]])
		# print("Generation number",result[2])
		time_taken = (stop-start)/5
		# print("Time Taken",time_taken)
		rarr.append([result[1],result[2],time_taken])



	itr.append(aaa)

# Basic GA
	number_of_parents = 2
	drule1=0
	drule2=0
	TimeGA(1,GA)

# Diploid GA
	number_of_parents = 2
	drule1=0
	drule2=0
	TimeGA(2,DGA)

# Multi-parent GA
	number_of_parents = 4
	drule1=0
	drule2=0
	TimeGA(1,MPGA)

# Dispatching Rules GA
	number_of_parents = 2
	drule1=1
	drule2=1
	TimeGA(1,DRGA)

# Final Enchanced GA
	number_of_parents = 2
	drule1=0
	drule2=0
	TimeGA(1)


# Function to Generate files
def writefile(name,arr):
	with open(name+".txt","w") as file :
		for i in range(len(arr)):
			output= str(itr[i])+" "+str(arr[i][0])+" "+str(arr[i][1])+" "+str(arr[i][2])
			file.write(output)
			file.write("\n")

writefile("GA",GA)
writefile("DGA",DGA)
writefile("DRGA",DRGA)
writefile("EGA",EGA)
writefile("MPGA",MPGA)


# Generation comparision

# with open("GEN.txt","w") as file :
# 	for i in range(len(GEN)):
# 		output= str(GEN[i])+" "+str(FIT[i])
# 		file.write(output)
# 		file.write("\n")
