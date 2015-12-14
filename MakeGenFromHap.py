import random
f = open('ACEHaploPairs.txt','r')
lines = f.readlines()

#g = [[0 for x in range(1)] for x in range(52)] 
gens = []
# If we need to read line 33, and assign it to some variable
row = int(lines[0])
base= int(lines[1])
#for x in xrange(2,24):
#	print(lines[x])
#print lines[2][0]
#r=random.randint(2,23)
#print r
haps=[]
for x in xrange(1,12):
	g=[]

#	r1=random.randint(2,row+1)
#	r2=random.randint(2,row+1)
	r1=2*x
	r2=2*x+1

	haps.append(r1)
	haps.append(r2)

	while (r2==r1):
		r2=random.randint(2,row+1)
	l1=lines[r1]
	l2=lines[r2]

	#print l1[3]
	#print l2[3]
	#if (l1[3]=='1'):
	#	print "it is"
	#	g.insert(0,1)
	#	print g[0]
	for y in xrange(0,base):
		if (l1[y]=='1' and l2[y]=='1'):
			g.append(1)
			
		if (l1[y]=='0' and l2[y]=='0'):
			g.append(0)
			
		if ((l1[y]=='0' and l2[y]=='1') or (l1[y]=='1' and l2[y]=='0')):
			g.append(2)
			
  # for z1 in xrange(1,3):
   	#for z2 in xrange(0,52):  
	#	print g[z]
	gens.append(g)


		#print g[x-1][y]
print "******************"
gen_file = open("ACEGen.txt",'w')
#gen_file.write(str(len(gens))+"\n")
for gen in gens:
	for pos in gen:
		gen_file.write(str(pos))
	gen_file.write("\n")
gen_file.close()

hap_file = open("ACEHAP.txt",'w')
for hap in haps:
	haplotype = lines[hap]
	for pos in haplotype:
		hap_file.write(str(pos))
hap_file.close()
print gens
