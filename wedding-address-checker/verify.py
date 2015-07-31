#!/usr/bin/env python
# Usage
# VIA: https://lob.com/blog/verify-shipping-addresses-in-python-for-free
# Very light tweaks to parse Google Drive doc.

# python verify.py input.csv

from __future__ import absolute_import, division, print_function, unicode_literals

import lob
import csv
import sys


with open('secret.key', 'r') as secret_key:
	lob.api_key = secret_key.read()


skipFirstLine  = True

country     = 'US'

try:
	sys.argv[1]
except IndexError:
	print("Please provide an input CSV file as an argument.")
	sys.exit()

# Open input files
inputFile = open(sys.argv[1], 'rU')
csvInput = csv.reader(inputFile)

# Create output files
errors = open('errors.csv', 'w')
verified = open('verified.csv', 'w')

# Loop through input CSV rows
for idx, row in enumerate(csvInput):
	if skipFirstLine and idx == 0:
		continue

	# Sanity check
	sys.stdout.write('Running.\n')
	sys.stdout.flush()

	try:
		name = row[0]
		print(name)
		city, stateandzip = row[2].split(',', 1)
		state, postcode = stateandzip.rsplit(' ', 1)
		verifiedAddress = lob.Verification.create(
			address_line1 = row[1],
			address_line2 = '',
			address_city = city,
			address_state = state,
			address_zip = postcode,
			address_country = country
		)
		# print(verifiedAddress)
	except Exception, e:
		outputRow = ",".join(row) + "," + str(e)+ "\n"
		errors.write(outputRow)
	else:
		outputRow = name + ","
		outputRow += verifiedAddress.address.address_line1 + ","
		outputRow += verifiedAddress.address.address_line2 + ","
		outputRow += verifiedAddress.address.address_city + ","
		outputRow += verifiedAddress.address.address_state + ","
		outputRow += verifiedAddress.address.address_zip + "\n"
		verified.write(outputRow)

errors.close()
verified.close()
print("\n")

