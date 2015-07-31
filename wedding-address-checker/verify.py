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

	try:
		name = row[0]
		print(name)
		address1 = row[1].strip().upper()
		city, stateandzip = row[2].split(',', 1)
		city = city.strip().upper()
		state, postcode = stateandzip.rsplit(' ', 1)
		state = state.strip().upper()
		postcode = postcode.strip()
		verifiedAddress = lob.Verification.create(
			address_line1 = address1,
			address_line2 = '',
			address_city = city,
			address_state = state,
			address_zip = postcode,
			address_country = country
		)
		if address1 != verifiedAddress.address.address_line1:
			print('\taddress_1 changed')
			print('\t\t', address1)
			print('\t\t', verifiedAddress.address.address_line1)
		if city != verifiedAddress.address.address_city:
			print('\tcity changed')
			print('\t\t', city)
			print('\t\t', verifiedAddress.address.address_city)
		if state != verifiedAddress.address.address_state:
			print('\tstate changed')
			print('\t\t', state)
			print('\t\t', verifiedAddress.address.address_state)
		if postcode != verifiedAddress.address.address_zip[0:5]:
			print('\tzip changed')
			print('\t\t', postcode)
			print('\t\t', verifiedAddress.address.address_zip[0:5])
		print('*********')
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

