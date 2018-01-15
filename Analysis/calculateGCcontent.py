#!/usr/bin/python

''' This script reads a GenBank file and calculates the GC content 
	of the coding sequence''' 

import os
from Bio import SeqIO
# Define input path
input_path = '' #('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
	#'sequence_files/Python-programming-for-life-science-researchers/Analysis')

# Change directory if specified
if input_path != '':
	os.chdir(input_path)
# File for testing function
GenBank_file = 'NC_001224.1.gb'
# Define a function that calculates GC content
def GC_content(GenBankFile):
	# Open Genbank file
	with open(GenBankFile, 'r') as fh:
			record = SeqIO.read(fh, 'genbank')
			#print len(record.seq)
			count = 0
			coding_sequence = ''
			# Check if CDS annotation present in GenBank file
			for feature in record.features:
				if feature.type == 'CDS':
					count += 1
					#print feature.location
					#print len(feature.location.extract(record).seq)
					coding_sequence += feature.location.extract(record).seq
				else:
					continue
			if count == 0:
				print 'No annotation information in file', GenBankFile
			else:
				GC = sum(coding_sequence.count(nucleotide) for nucleotide in ['G','C','g','c'])
				try:
					return GC * 100.00 / len(coding_sequence)
				except ZeroDivisionError:
					return 0.0
print 'GC-content: %f' % GC_content(GenBank_file)




