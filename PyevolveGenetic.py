from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Selectors
from pyevolve import Initializators, Mutators
from pyevolve import G2DList
from pyevolve import Crossovers
import genError

global Genes
Genes= []
global first_gen
first_gen = []

def read_gens():
	global Genes
	gens_file = open("ACEGen.txt","r")
	lines = gens_file.readlines()
	for i in range(0,len(lines)):
		gen = []
		print lines[i]
		for j in range(len(lines[i])-1):
			gen.append(int(lines[i][j]))
		print len(gen)
		Genes.append(gen)
	print "Genes"
	print Genes



def read_first_pop():
	global first_gen
	count = 0
	line = ""
	input_file = open("Out_ACEGEN.txt")
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
				first_gen.append(pop)			
				pop = []
				count = 0
				input_file.readline()
		else:
			break

# Find negative values
def eval_func(ind):
	score = 0
	for x in range(0,4):
		for y in range(0,4):
			if ind[x][y] == 0: 
				score += 1
	return score
    

def check_combined(x1, x2, y):
	for i in range(len(y)):
		if(y[i]==0):
			if (x1[i]!=0 or x2[i]!=0):
				return False
		elif (y[i]==1):
			if (x1[i]!=1 or x2[i]!=1):
				return False
		else:
			if (x1[i]==x2[i]):
				return False
	return True


def eval_hap(chromosome):
	score = 0
	number = len(chromosome[:][:])
	for i in range(number):
		for j in range(i+1,number):
			if chromosome[i]==chromosome[j]:
				score+=1
				#print "*****"
	#global Genes
	number_of_genes = len(Genes)
	for i in range(number_of_genes):
		if(check_combined(chromosome[2*i],chromosome[2*i+1],Genes[i])):
			#print "*****"
			score +=5
	return score
	
def evolve_callback(ga):
	generation = ga.getCurrentGeneration()
	global first_gen
	if generation == 1:
		pop = ga.getPopulation()
		for i in range (0,80):
			for j in range (0,10):
				for k in range(0,52):
					pop[i][j][k] = first_gen[i][j][k]
	if generation%100 == 0 or generation==0: 
		print "generation: ", generation
		print ga.bestIndividual()

	return False




def main():    
	global Genes
	global first_gen

	read_gens()

	read_first_pop()

	genome = G2DList.G2DList(2*len(Genes),len(Genes[0]))
	genome.setParams(rangemin=0, rangemax=1)


	genome.crossover.set(Crossovers.G2DListCrossoverSingleHPoint)
	genome.mutator.set(Mutators.G2DListMutatorIntegerGaussian)

	genome.evaluator.set(eval_hap)

	# Genetic Algorithm Instance
	ga = GSimpleGA.GSimpleGA(genome)
	ga.selector.set(Selectors.GRouletteWheel)
	ga.nGenerations = 50
	ga.stepCallback.set(evolve_callback)
	# Do the evolution
	ga.evolve()

	# Best individual
	l = ga.bestIndividual()
	hapFile = open("ACEHAP_Result.txt",'w')
	for row in l:
		line=""
		for char in row:
			line+=str(char)
		hapFile.write(line+"\n")
	hapFile.close()
	
	genError.clac_genotype_error()
	genError.calc_switch_error()
		
if __name__ == "__main__": 
	main()