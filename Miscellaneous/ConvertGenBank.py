#!/usr/bin/python

### This script converts GenBank files to FASTA (.fna) format ###

# import os module to enable handling of OS funtionalities 
import os
# Import the sequence input/output module from biopython
from Bio import SeqIO

input_dir = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			 'sequence_files/Python-programming-for-life-science-researchers/Miscellaneous')
output_dir = ('/Users/malcarl/Documents/Courses/python-programming-for-life-science-researchers/'
			 'sequence_files/Python-programming-for-life-science-researchers/Miscellaneous')
# list all GenBank files
GenBank_files = []
for filename in os.listdir(input_dir):
	if filename.endswith('.gb'):
		GenBank_files.append(filename)

# Construct list of RefSeq IDs
IDs = []
for filename in GenBank_files:
	pos_extension = filename.find('.gb')
	ID = filename[:pos_extension]
	IDs.append(ID)

# Construct FASTA file from GenBank file
os.chdir(output_dir)
count = 0

for file in GenBank_files:
	count += 1
	print 'Processing file %d of %d' % (count, len(IDs))
	try:
		with open(os.path.join(input_dir,file),'r') as input_file, open(IDs[count-1] + '.fna','w') as output_file:
			for seq_record in SeqIO.parse(input_file,"genbank"):
				print 'Dealing with GenBank ID %s' % seq_record.id
				output_file.write('>%s %s\n%s' % (seq_record.id,
						seq_record.description,
						seq_record.seq))
	except:
		print 'Failed'