#!/usr/bin/python

''' Script for obtaining GenBank file for all Saccharomyces cerevisiae 
    strains with mitochondrial genome sequences available. The script
    starts from two genome lists, one with mitochondrial genomes and
    one with complete organism genome, and then uses ftplib to download 
    gbff files with sequence information for the entire organism genome'''

import os
from ftplib import FTP
import re
import gzip

# Define directory where gene list are present
input_dir = '' #('/Users/malcarl/Documents/Courses/'
	#'python-programming-for-life-science-researchers/sequence_files/'
	#'Python-programming-for-life-science-researchers/DownloadGenomeGenBanks')
# Define directory for output files
output_dir = '' #('/Users/malcarl/Documents/Courses/'
	#'python-programming-for-life-science-researchers/sequence_files/'
	#'Python-programming-for-life-science-researchers/DownloadGenomeGenBanks')
# Specify name of genome lists
mito_Genome_List = 'MitoGenomeList.txt'
Genome_List = 'GenomeList.txt'

# Move to input directory if specified
if input_dir != '':
	os.chdir(input_dir)

# Create lists to store strain name
strain_names_MT = []
# Create empty list to store GenBank assembly accession IDs
GenBank_assembly = []
# open and read mitochondrial genomes list
with open(mito_Genome_List,'r') as MitoGenomeList:
	for entry in MitoGenomeList:
		entry = entry.strip()
		# Assign organism name and strain name to lists
		if not entry.startswith('#'):
			strain_name = entry.split('\t')[2]
			strain_names_MT.append(strain_name)

# Open file with genome list and compare strains to mitochondrial genomes
with open(Genome_List,'r') as GenomeList:
	for entry in GenomeList:
		entry = entry.strip()
		org_name = entry.split('\t')[0]
		strain_name = entry.split('\t')[2]
		# Check if mitochondrial genome for strain is available
		if strain_name in strain_names_MT:
			assembly_ID = entry.split('\t')[3]
			GenBank_assembly.append(assembly_ID)

# Download gbff file from NCBI using ftplib
# Specify connection details
server = 'ftp.ncbi.nlm.nih.gov'
parent_directory = 'genomes/genbank/fungi/Saccharomyces_cerevisiae/latest_assembly_versions/'

# Connect to server
ftp = FTP(server)
ftp.login()

# Change directory to where the files are found
ftp.cwd(parent_directory)
directories = []
# List files in directory
ftp.retrlines('LIST', directories.append)

# Go through list of drectories to find full assembly ID including version
assembly_ID_full = []
for directory in directories:
	for ID in GenBank_assembly:
		pattern = ID + '.*'
		expr = re.compile(pattern)
		result = expr.search(directory)
		if result:
			new_result = result.group(0)
			new_result = new_result.split()[0]
			#print new_result
			assembly_ID_full.append(new_result)

# Change to output directory if specified
if output_dir != '':
	os.chdir(output_dir)

# Download gbff file for each assembly
for assembly in assembly_ID_full:
	# Change to directory for the assembly ID. This follows a link to
	# /genomes/all/GCA/*
	ftp.cwd(assembly)
	filename = assembly + '_genomic.gbff.gz'
	# open file for writing gbff file to
	with open(filename,'wb') as outfile:
		try:
			ftp.retrbinary('RETR ' + filename, outfile.write)
		except:
			print 'Could not retrieve file', filename
	# change back to parent_directory
	ftp.cwd('../../../../../../genbank/fungi/Saccharomyces_cerevisiae/latest_assembly_versions/')
	# Specify filename for unzipped files
	new_filename = assembly + '_genomic.gbff'
	with gzip.open(filename, 'rb') as inFile, open(new_filename, 'wb') as outFile:
		try:
			file_content = inFile.read()
		except:
			print 'Couldn\'t read file', filename 
		try:
			outFile.write(file_content)
		except:
			print 'Couldn\'t write file', new_filename

# Close connection
ftp.quit()

current_dir = os.getcwd()

# remove compressed files after unzipping
for file in os.listdir(current_dir):
	if file.endswith('.gz'):
		os.remove(file)
