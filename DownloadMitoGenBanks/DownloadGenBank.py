#!/usr/bin/python

''' This script downloads GenBank files from NCBI using Entrez from biopython. The input file is a list of
	mitochondrial genomes dowloaded from NCBI Genomes '''

# Import the Entrez module from biopython
from Bio import Entrez as entrez

# Import os module to enable OS functionalities
import os

# Specify the directory of the input file
input_dir = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/sequence_files/'
	'Python-programming-for-life-science-researchers/DownloadMitoGenBanks')
# Specify the output path for the GenBank files
output_dir = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/sequence_files/'
	'Python-programming-for-life-science-researchers/DownloadMitoGenBanks')
# Specify name of input file
input_file = 'MitoLocusIDs.txt'
# Move to input directory
os.chdir(input_dir)

# Create lists to store locus IDs and strain names
locusIDs = []
strain_name = []
# Read file containing locusIDs
count = 0
with open(input_file,'r') as infile:
	for line in infile:
		count += 1
		line = line.strip()
		ID = line.split('\t')[1]
		ID = ID.strip()
		strain = line.split('\t')[0]
		# Replace all whitespaces in strain name with underscore
		strain = strain.replace(' ','_')
		strain_name.append(strain)
		# Select ncbi ID if available
		if '/' in ID:
			pos_slash = ID.find('/')
			new_ID = ID[:pos_slash]
			locusIDs.append(new_ID)
		else:
			locusIDs.append(ID)

# Move to output directory
os.chdir(output_dir)

# Run Genbank query for all RefSeq IDs:
count = 0
num_IDs = len(locusIDs)
for index, ID in enumerate(locusIDs):
	name = strain_name[index]
	# Check if strain name already in file directory to avoid overwriting
	if name + '.gb' in os.listdir(output_dir):
		name = name + '_' + str(1) 
	with open(name + '.gb','w') as outfile:
		entrez.email = 'carl_malina@hotmail.com'
		gbFile = entrez.efetch(db = 'nucleotide', id = ID, rettype = 'gb')
		try:
			outfile.write(gbFile.read())
		except:
			print 'Cannot write to file'
			pass
	count += 1
	print 'Done with %d of %d IDs' % (count, num_IDs)

