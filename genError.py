def clac_genotype_error():
	haps1 = read_haplotypes("ACEHAP.txt")
	haps2 = read_haplotypes("ACEHAP_Result.txt")
	error = 0
	for i in range(len(haps1)/2):
		if haps1[2*i]!=haps2[2*i] and haps1[2*i]!=haps2[2*i+1]:
			error+=1
	print error
	print len(haps1)
	print 2.0*float(error)/(len(haps1))
def calc_switch_error():
	haps1 = read_haplotypes("ACEHAP200.txt")
	haps2 = read_haplotypes("ACEHAP_Result.txt")
	error = 0
	SNPcount = 0
	for i in range(len(haps1)/2):
		error1 = 0
		error2 = 0
		for j in range(len(haps1[2*i])):
			if haps1[2*i][j] != haps1[2*i+1][j]:
				SNPcount += 1
				if haps1[2*i][j] != haps2[2*i][j]:
					error1 += 1
				if haps1[2*i][j] != haps2[2*i+1][j]:
					error2 += 1
					
		if error1<error:
			error += error1
		else:
			error += error2
			
	print error
	print SNPcount
	print float(error)/float(SNPcount)
	
def read_haplotypes(fileName):
	haps = []
	hap_file = open(fileName)
	lines = hap_file.readlines()
	for line in lines:
		haps.append(line[:-1])
	return haps

