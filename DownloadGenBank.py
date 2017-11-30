#!/usr/bin/python

### This script downoads GenBank files from NCBI using Entrez from biopython ### 

# Check that the library is installed and that it can be loaded
try:
	from Bio import Entrez as entrez
except:
	print 'Cannot import Entrez'

with open('testFile.gb','w') as outfile:
	entrez.email = 'carl_malina@hotmail.com'
	gbFile = entrez.efetch(db = 'nucleotide', id = 'NC_002333.1', rettype = 'gb')
	try:
		outfile.write(gbFile.read())
	except:
		print 'Cannot write to file'
