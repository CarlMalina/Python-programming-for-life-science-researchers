#!/usr/bin/python

### This script downloads GenBank files from NCBI using Entrez from biopython ### 

# Import the Entrez module from biopython
from Bio import Entrez as entrez

# Import os module to enable OS functionalities
import os

# Specify the output path for the GenBank files
output_dir = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			  'sequence_files/Python-programming-for-life-science-researchers/GenBankFiles')
# Move to directory
os.chdir(output_dir)
locusIDs = []
# Read file containing locusIDs
count = 0
with open('fungalMitochondrialLocusIDs.txt','r') as infile:
	for line in infile:
		count += 1
		line = line.strip()
		ID = line.split('\t')[1]
		ID = ID.strip()
		# Select ncbi ID if available
		if '/' in ID:
			pos_slash = ID.find('/')
			new_ID = ID[:pos_slash]
			locusIDs.append(new_ID)
		else:
			locusIDs.append(ID)

# Run Genbank query for all RefSeq IDs:
count = 0
num_IDs = len(locusIDs)
for ID in locusIDs:
	with open(ID + '.gb','w') as outfile:
		entrez.email = 'carl_malina@hotmail.com'
		gbFile = entrez.efetch(db = 'nucleotide', id = ID, rettype = 'gb')
		try:
			outfile.write(gbFile.read())
		except:
			print 'Cannot write to file'
			pass
	count += 1
	print 'Done with %d of %d IDs' % (count, num_IDs)

