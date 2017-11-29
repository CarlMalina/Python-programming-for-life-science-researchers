#!/usr/bin/python

from ftplib import FTP

# Specify connection details
server = 'ftp.ncbi.nlm.nih.gov'
directory = 'genomes/refseq/mitochondrion/'
filename = 'mitochondrion.1.1.genomic.fna.gz'

# Connect to server
ftp = FTP(server)
ftp.login()

# Change directory to where the files are found
ftp.cwd(directory)

# List files in directory
ftp.retrlines('LIST')

# Download file from server
with open(filename,'wb') as outfile:
	try:
		ftp.retrbinary('RETR ' + filename, outfile.write)
	except:
		print 'Could not retrieve file', filename
ftp.quit()

# Uncompress the file
import gzip
with gzip.open(filename, 'rb') as inFile, open('mitochondrion.1.1.genomic.fna', 'wb') as outFile:

	try:
		file_content = inFile.read()
		outFile.write(file_content)
	except:
		print 'Couldn\'t read and/or write file', filename 
