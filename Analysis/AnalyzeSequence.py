#!/usr/bin/python

''' This script takes a GenBank file as input and calculates the codon usage
	and amino acid usage of the coding sequence of the genome. '''

from Bio import SeqIO
from Bio.Data import CodonTable
import os
import matplotlib.pyplot as plt

# Define the path for GenBank files

input_path = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			  'sequence_files/Python-programming-for-life-science-researchers/Analysis')
# Define path for output figures
output_path = '' #('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/sequence_files/'
	#'Python-programming-for-life-science-researchers/Analysis/Plots')
# In this example, the file for S. cerevisiae S288c mitochondrial genome is used for testing functionality
GenBank_file = 'NC_001224.1.gb'

def count_codons(GenBankFile):
	
	# Open and read the GenBank file using SeqIO
	with open(GenBankFile, 'r') as fh:
		record = SeqIO.read(GenBankFile, 'genbank')

		# Extract coding sequences
		count = 0 
		total_coding_sequence = ''
		for feature in record.features:
			if feature.type == 'CDS':
				count += 1
				total_coding_sequence += feature.location.extract(record).seq
				# Get translation table ID
				if 'translation_table' in feature.qualifiers:
					translation_table_id = int(feature.qualifiers['transl_table'][0])
				else: 
					translation_table_id = 1 # Standard genetic code

		# Check if CDS annotation present in GenBank file
		if count == 0:
			print 'No coding sequence annotation in file', GenBankFile
			return

		# Make sure sequence is upper case
		if str(total_coding_sequence).islower():
			sequence = str(total_coding_sequence).upper()
		else:
			sequence = str(total_coding_sequence)

		# Load translation table from NCBI
		translation_table = CodonTable.unambiguous_dna_by_id[translation_table_id] 
		# Initiate dictionary with all codons, used for counting
		CodonsDict = {}
		for key, value in translation_table.forward_table.items():
			CodonsDict[key] = 0
		# Add stop codons (not included in initial table)
		for codon in translation_table.stop_codons:
			CodonsDict[codon] = 0

		# Create a dictionary with synonymous codons
		Synonymous_Codons = CodonTable.unambiguous_dna_by_id[translation_table_id].forward_table 
		for codon in CodonTable.unambiguous_dna_by_id[translation_table_id].stop_codons: 
			Synonymous_Codons[codon] = 'Stop' 

		# Change single letter to three letter abbreviations
		for key,value in Synonymous_Codons.items():
			if value == 'F':
				Synonymous_Codons[key] = 'Phe'
			elif value == 'L':
				Synonymous_Codons[key] = 'Leu'
			elif value == 'T':
				Synonymous_Codons[key] = 'Thr'
			elif value == 'I':
				Synonymous_Codons[key] = 'Ile'
			elif value == 'M':
				Synonymous_Codons[key] = 'Met'
			elif value == 'V':
				Synonymous_Codons[key] = 'Val'
			elif value == 'S':
				Synonymous_Codons[key] = 'Ser'
			elif value == 'P':
				Synonymous_Codons[key] = 'Pro'
			elif value == 'A':
				Synonymous_Codons[key] = 'Ala'
			elif value == 'Y':
				Synonymous_Codons[key] = 'Tyr'
			elif value == 'H':
				Synonymous_Codons[key] = 'His'
			elif value == 'Q':
				Synonymous_Codons[key] = 'Gln'
			elif value == 'N':
				Synonymous_Codons[key] = 'Asn'
			elif value == 'K':
				Synonymous_Codons[key] = 'Lys'
			elif value == 'D':
				Synonymous_Codons[key] = 'Asp'
			elif value == 'E':
				Synonymous_Codons[key] = 'Glu'
			elif value == 'C':
				Synonymous_Codons[key] = 'Cys'
			elif value == 'W':
				Synonymous_Codons[key] = 'Trp'
			elif value == 'R':
				Synonymous_Codons[key] = 'Arg'
			elif value == 'G':
				Synonymous_Codons[key] = 'Gly'
			else:
				continue

		# Iterate over sequence and count codon occurence
		for i in range(0, len(sequence), 3):
			codon = sequence[i:i + 3]
			if codon in CodonsDict:
				CodonsDict[codon] += 1
			else:
				print 'Invalid codon %s in sequence' % codon
		
		# Calculate the usage of each codon in % of total codons
		codon_usage_percent = {}
		codon_usage = CodonsDict
		tot_codons = sum(CodonsDict.values())
		for key,value in CodonsDict.items():
			codon_usage_percent[key] = 100.00 * value / tot_codons

		#for key, value in codon_usage_percent.items():
		#	print key, value
		#print codon_usage

		# Initialize a dictionary for counting amino acid occurence
		amino_acid_occurence = {}
		amino_acid_usage = {}
		for codon, aa in Synonymous_Codons.items():
			amino_acid_occurence[aa] = 0
		#print amino_acid_occurence, len(amino_acid_occurence)
		
		# Count the occurence of each amino acid		
		for amino_acid in amino_acid_occurence:
			amino_acid_sum = 0
			for codon, aa in Synonymous_Codons.items():
				if aa == amino_acid:
					amino_acid_sum += codon_usage[codon]		
			amino_acid_occurence[amino_acid] = amino_acid_sum
		total_amino_acids = sum(amino_acid_occurence.values())
		for aa, value in amino_acid_occurence.items():
			amino_acid_usage[aa] = 100.00 * value / total_amino_acids
		#print amino_acid_usage

		#for key,value in amino_acid_usage.items():
		#	print key, value
		# Change to directory for output plots
		if output_path != '':
			os.chdir(output_path)
		else:
			pass
		# Plot codon and amino acid usage and save as file
		plt.figure(figsize=(10,5))
		plt.bar(range(len(codon_usage_percent)), codon_usage_percent.values(), align = 'center', alpha = 0.5)
		plt.xticks(range(len(codon_usage)), codon_usage.keys(), rotation = 'vertical')
		plt.ylabel('Frequency (%)')
		plt.xlabel('Codon')
		plt.tick_params(axis='x', which='both', labelsize=7)
		name = GenBankFile.split('.gb')[0]
		title1 = 'Codon_usage_' + name + '.png'
		plt.savefig(title1,bbox_inches = 'tight')

		plt.figure(figsize=(10,5))
		plt.bar(range(len(amino_acid_usage)), amino_acid_usage.values(), align = 'center', alpha=0.5)
		plt.xticks(range(len(amino_acid_usage)), amino_acid_usage.keys()) #rotation = 'vertical')
		plt.ylabel('Frequency (%)')
		plt.xlabel('Amino acid')
		plt.tick_params(axis='x', which='both', labelsize=7)
		title2 = 'Amino_acid_usage_' + name + '.png'
		plt.savefig(title2,bbox_inches = 'tight')

		# Change directory to input directory
		os.chdir(input_path)

		return codon_usage, amino_acid_usage

count_codons(GenBank_file)

