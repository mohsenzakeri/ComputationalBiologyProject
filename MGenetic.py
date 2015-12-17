import random
import genError

population = 80


#Evaluation Function which tries to maximize the number of similar haplotypes.
#The set of haplotypes with larger number of similar haplotypes will receive a higher score.
def eval_hap(individual):
	score = 0
	number = len(individual[:][:])
	for i in range(number):
		for j in range(i+1,number):
			if individual[i]==individual[j]:
				score+=1
				#print "*****"	
	return score

def eval_hap1(individual):
	score = 0
	number = len(individual[:][:])
	for i in range(number/2):
		for j in range(i+2, number):
			snp = 0
			for k in range(len(individual[2*i])):
				if individual[2*i][k]==individual[j][k]:
					snp+= 1
			score += float(snp)/float(len(individual[2*i]))
	return score
	

#This structure helps to sort the individuals based on their score to 
class FitnessIndividual:
	def __init__(self,score,ind):
		self.fitness = score
		self.individual = ind


#This class is for keeping track of population of every generation and the best individual in the generatoin.
class Generation:
	def __init__(self, individuals, number):
		self.individuals = individuals
		self.number = number
		self.bestScore = -1
		self.bestIndividual = None

	def findBestIndividual(self):
		self.bestScore = -float('inf')
		for individual in self.individuals:
			if self.bestScore < eval_hap(individual):
				self.bestScore = eval_hap(individual)
				self.bestIndividual = individual


#This function reads the first population which is the result of running collhaps algorithm.
#It reads some individuals for selecting in every step of genetic algorithm in "nextGenerations_collHapse".
def read_first_pop():
	global first_gen
	global nextGenerations_collHapse
	count = 0
	line = ""
	input_file = open("Out_ACEGEN50.txt")
	pop = []
	line = input_file.readline()
	gen_count = int(line)
	while(True):
		line = input_file.readline()
		if line:
			string_row = line[:-1]
			int_row = []
			for i in range(len(string_row)):
				int_row.append(int(string_row[i]))
			pop.append(int_row)
			
			count +=1
			if count == gen_count:
				if (len(first_gen)<population):
					first_gen.append(pop)			
				else:
					nextGenerations_collHapse.append(pop)
				pop = []
				count = 0
				input_file.readline()
		else:
			break

#Mutates the SNP sites of an individual by some probability.
def mutate(individual):
	new_individual = []
	for i in range(0,len(individual)/2):
		new_hap1 = []
		new_hap2 = []
		for j in range(0,len(individual[2*i])): #base
			if(individual[2*i][j]==individual[2*i+1][j]):
				new_hap1.append(individual[2*i][j])
				new_hap2.append(individual[2*i][j])
			else:
				if random.random()<0.5: #Some Probability
					new_hap1.append(individual[2*i+1][j])
					new_hap2.append(individual[2*i][j])
				else:
					new_hap1.append(individual[2*i][j])
					new_hap2.append(individual[2*i+1][j])

		new_individual.append(new_hap1)
		new_individual.append(new_hap2)
	return new_individual

#Doing Crossover for genetic steps. In this function some haplotype pairs are randomly chosen and interchanged between two indivudulas to 
#generate two new individuals.
def crossOver(individual1, individual2):
	tempInd1 = []
	tempInd2 = []

	for row in individual1:
		tempInd1.append(row)

	for row in individual2:
		tempInd2.append(row)

	genotypeCount = len(tempInd1)/2

	startCross = int(random.random()*genotypeCount)	
	endCross = startCross
	while(endCross==startCross):	
		endCross = int(random.random()*genotypeCount)
	
	if startCross>endCross:
		startCross, endCross = endCross, startCross

	crossed1 = []
	crossed2 = []

	for i in range(startCross, endCross):
		tempInd1[2*i], tempInd2[2*i] = tempInd2[2*i] , tempInd1[2*i]
		tempInd1[2*i+1], tempInd2[2*i+1] = tempInd2[2*i+1] , tempInd1[2*i+1]

	return tempInd1, tempInd2

#Choosing some of individuals randomly from previous generation.
def getFromPrevGen(generation, k):
	#Let's try randomly choosing
	tempGen = []
	for pop in generation:
		tempGen.append(pop)
	selected = []
	for i in range(k):
		choice = random.choice(tempGen)
		selected.append(choice)
		tempGen.remove(choice)
	return selected

#Selecting best k individuals of a generation based on eval_hap.
def getBestK(generation, k):
	fitList = []
	for pop in generation:
		score = eval_hap(pop)	
		fitnessInd = FitnessIndividual(score, pop)
		fitList.append(fitnessInd)

	sorted_list = sorted(fitList, key= lambda x: x.fitness, reverse = True)
	result = []
	for i in range(k):
		result.append(sorted_list[i].individual)
	return result

#Mutate generatoin and returns the best k mutated individuals
def getBestMutated(generation, k):
	mutated = []
	for pop in generation:
		mutated.append(mutate(pop))
	return getBestK(mutated, k)

#Generate new indivudulas from previous generation by crossing over the previous individals
#Randomly choose pairs of individals.
def getBestCrossover(generation, k):
	tempGen = []
	for pop in generation:
		tempGen.append(pop)

	randomized = []
	for i in range(len(generation)):
		choice = random.choice(tempGen)
		randomized.append(choice)
		tempGen.remove(choice)

	crossOveres = []
	for i in range(len(randomized)/2):
		c1 , c2 = crossOver(randomized[2*i],randomized[2*i+1])
		crossOveres.append(c1)
		crossOveres.append(c2)
	
	
	return getBestK(crossOveres, k)

#Select some individuals from collhaps results in every genetic iteration.
def getFromCollhapse(generationNumber, k):
	global nextGenerations_collHapse
	selected = []
#	for i in range((generationNumber-1)*k, generationNumber*k):
#		selected.append(nextGenerations_collHapse[i])
	for i in range(k):
		choice = random.choice(nextGenerations_collHapse)
		selected.append(choice)
	return selected


def generateNextGeneration(generation, generationNumber):
	bestMutated = getBestMutated(generation, 20)
	bestCrossovers = getBestCrossover(generation,20)		
	prevGenSelection = getFromPrevGen(generation, 20) 
	collHapseSelection = getFromCollhapse(generationNumber, 20)
	nextGenGenerator =  bestMutated + bestCrossovers + prevGenSelection + collHapseSelection

	bestK = getBestK(nextGenGenerator, 30)

	fitList = []
	for pop in generation:
		fitInd = FitnessIndividual(eval_hap(pop),pop)
		fitList.append(fitInd)

	sorted_list = sorted(fitList, key= lambda x: x.fitness)
	nextGen = []
	for i in range(population):
		if(i<2):
			nextGen.append(bestK[i])
		else:
			nextGen.append(sorted_list[i].individual)
	
	return nextGen	
	
#Runs genetic iterations "minRun" times.
def runGenetic(minRun):
	global first_gen
	counter = 0
	generations = []
	first = Generation(first_gen, 0)
	first.findBestIndividual()
	generations.append(first)
	while(True):
		newGenerationIndividuals = generateNextGeneration(generations[counter].individuals, counter+1)
		counter += 1
		newGeneration = Generation(newGenerationIndividuals, counter+1)
		newGeneration.findBestIndividual()
		if counter%10==0:
			print newGeneration.bestScore
		generations.append(newGeneration)
		if counter>minRun:
			#check Convergance
			return generations[counter-1]

#Function for printing an entire generatoin by the score of each individual
def printGeneration(generation):
	for pop in generation:
		for row in pop:
			print pop
		print eval_hap(pop)
		print "*******************"


def main():
	global first_gen
	global nextGenerations_collHapse

	first_gen = []
	nextGenerations_collHapse = []
	
	read_first_pop()
	generation = runGenetic(50)
	bestIndividual = generation.bestIndividual
	

	
	hap_file = open("ACEHAP_Result.txt",'w')
	for hap in bestIndividual:
		for pos in hap:
			hap_file.write(str(pos))
		hap_file.write("\n")

	number = len(bestIndividual[:][:])

	
	hap_file.close()

	genError.clac_genotype_error()
	genError.calc_switch_error()

if __name__ == "__main__": 
	main()