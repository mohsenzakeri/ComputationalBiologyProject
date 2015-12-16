import random

def makeGenotypes(fileName):
	f = open(fileName)
	lines = f.readlines()

	gens = []
	row = int(lines[0])
	base= int(lines[1])
	haps=[]
	for x in xrange(1,21): #Insert the desired number of genotypes here.
		gen =[]

		#To select two haplotype from dataset to generate a genotype
		r1=random.randint(2,row+1)
		r2=random.randint(2,row+1)
		while (r2==r1):
			r2=random.randint(2,row+1)
			
		#For selecting haplotypes nonrandomly.
		#r1=2*x
		#r2=2*x+1	
		
		l1=lines[r1]
		l2=lines[r2]
		
		#To store the selected haplotype to generate current genotype
		haps.append(l1)
		haps.append(l2)

		for y in xrange(0,base):
			if (l1[y]=='1' and l2[y]=='1'):
				gen.append(1)
			
			if (l1[y]=='0' and l2[y]=='0'):
				gen.append(0)
			
			if ((l1[y]=='0' and l2[y]=='1') or (l1[y]=='1' and l2[y]=='0')):
				gen.append(2)			
		gens.append(gen)
	return (gens,haps)

def  outputGeneratedGensHaps(gens, haps, genFile, hapFile):
	gen_file = open(genFile,'w')
	for gen in gens:
		for pos in gen:
			gen_file.write(str(pos))
		gen_file.write("\n")
	gen_file.close()

	hap_file = open(hapFile,'w')
	for hap in haps:
		for pos in hap:
			hap_file.write(str(pos))
	hap_file.close()
	#print gens
	
def main():
	(gens, haps) = makeGenotypes("ACEHaploPairs.txt")
	outputGeneratedGensHaps(gens, haps, "ACEGEN20.txt", "ACEHAP20.txt")

if __name__ == "__main__": 
	main()
