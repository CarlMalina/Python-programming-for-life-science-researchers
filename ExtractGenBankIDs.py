#!/usr/bin/python

# Import os module to enable OS functionalities
import os

# Define input and output paths
input_path = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			  'sequence_files/Python-programming-for-life-science-researchers')
output_path = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			   'sequence_files/Python-programming-for-life-science-researchers/GenBankFiles')

# Change directory
os.chdir(input_path)
# Extract the RefSeq IDs from the organelle genome file:
locusIDs = []
organism_names = []

with open('mitochondrial_genomes_funghi.txt', 'r') as inFile:
	for line in inFile:
		if not line.startswith('#'):
			# Get organism name
			organism = line.split('\t')[0]
			organism_names.append(organism)
			# Get locus information
			ID = line.split('\t')[6]
			if ':' in ID:
				pos_colon = ID.find(':')
				new_ID = ID[pos_colon + 1:len(ID)]
				locusIDs.append(new_ID)
			else:
				locusIDs.append(ID)

# Change directory
os.chdir(output_path)
# Write organism name and GenBankID to a file:
with open('fungalMitochondrialLocusIDs.txt','w') as outfile:
	for index, item in enumerate(organism_names):
		try:
			outfile.write(item + '\t ' + locusIDs[index] + '\n')
		except:
			print 'Failed to write file'
			