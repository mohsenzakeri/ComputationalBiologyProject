import random
import genError

population = 80

class FitnessIndividual:
	def __init__(self,score,ind):
		self.fitness = score
		self.individual = ind



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

def read_first_pop():
	global first_gen
	global nextGenerations_collHapse
	count = 0
	line = ""
	input_file = open("ACEGen200.txt")
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
				#print pop
				if (len(first_gen)<population):
					first_gen.append(pop)			
				else:
					nextGenerations_collHapse.append(pop)
				pop = []
				count = 0
				input_file.readline()
		else:
			break

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
				if random.random()<0.05:
					new_hap1.append(individual[2*i+1][j])
					new_hap2.append(individual[2*i][j])
				else:
					new_hap1.append(individual[2*i][j])
					new_hap2.append(individual[2*i+1][j])

		new_individual.append(new_hap1)
		new_individual.append(new_hap2)
	return new_individual


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
			for k in range(len(individual[2*i])):
				if individual[2*i][k]==individual[j][k]:
					score+=1
	return score
	
	
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


def getBestMutated(generation, k):
	mutated = []
	for pop in generation:
		mutated.append(mutate(pop))
	return getBestK(mutated, k)


def getFromCollhapse(generationNumber, k):
	global nextGenerations_collHapse
	selected = []
#	for i in range((generationNumber-1)*k, generationNumber*k):
#		selected.append(nextGenerations_collHapse[i])
	for i in range(k):
		choice = random.choice(nextGenerations_collHapse)
		selected.append(choice)
	return selected

def printGeneration(generation):
	for pop in generation:
		for row in pop:
			print pop
		print eval_hap(pop)
		print "*******************"

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

def generateNextGeneration(generation, generationNumber):
	bestMutated = getBestMutated(generation, 20)
	bestCrossovers = getBestCrossover(generation,20)
		
	prevGenSelection = getFromPrevGen(generation, 20)
	collHapseSelection = getFromCollhapse(generationNumber, 20)
	nextGenGenerator = bestMutated + bestCrossovers + prevGenSelection + collHapseSelection

	bestK = getBestK(nextGenGenerator, 2)

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
		if counter%1==0:
			print newGeneration.bestScore
		generations.append(newGeneration)
		if counter>minRun:
			#check Convergance
			return generations[counter-1]



def main():
	global first_gen
	global nextGenerations_collHapse

	first_gen = []
	nextGenerations_collHapse = []

	read_first_pop()
	print "first gen"
	print len(first_gen)
	generation = runGenetic(200)
	bestIndividual = generation.bestIndividual

	hap_file = open("ACEHAP_Result.txt",'w')
	for hap in bestIndividual:
		for pos in hap:
			hap_file.write(str(pos))
		hap_file.write("\n")
		
	hap_file.close()

	genError.clac_genotype_error()
	genError.calc_switch_error()

if __name__ == "__main__": 
	main()