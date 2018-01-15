#!/usr/bin/python

# Check if sequence present in Genbank file
input_path = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
	'sequence_files/Python-programming-for-life-science-researchers/Miscellaneous')

import os
# Change directory
os.chdir(input_path)
files = os.listdir(input_path)
files_without_sequence = []

for file in files:
	if not file.endswith('.gb'):
		continue
	with open(file, 'r') as inFile:
		content = inFile.read()
		if not 'ORIGIN' in content:
			print 'sequence not in file', file
			files_without_sequence.append(file)

# Write name of GenBank files without sequence to file
if len(files_without_sequence) > 0:
	with open('GenBanks_without_sequence.txt', 'w') as outFile:
		for item in files_without_sequence:
			pos_file_extension = item.find('.gb')
			ID = item[:pos_file_extension] 
			outFile.write(ID + '\n')

