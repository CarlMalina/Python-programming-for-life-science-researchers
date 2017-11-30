#!/usr/bin/python

# First, extract the RefSeq IDs from the organelle genome file

refSeqIDs = {}
with open('test.txt', 'r') as inFile:
	#content = genomeInfoFile.read()
	for line in inFile:
		if line.startswith('#'):
			continue
		else:
			organism = line.split('\t')[0]
			ID = line.split('\t')[4]
			refSeqIDs[organism] = ID

for key,value in refSeqIDs.items():
	print key + ': ' + value
			