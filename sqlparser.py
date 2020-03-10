#This Script is meant to automate the additon of SQL data using a JSON file.
import mysql.connector 
from mysql.connector import errorcode
import json
import os

msql_config = {
	"user": "me",
	"password": "passwd",
	"host": "localhost",
	"database": "TaxRates", #TaxRates
	"raise_on_warnings": True	
}

try: 
	link = mysql.connector.connect(**msql_config)
except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Invalid username or password. ")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database doesn't exist. ")
		else: 
			print(err)
else:

	cursor = link.cursor()



	#load json into a dictionary var
	with open('taxRates.json') as tax_rates: # or tax_rates = open('taxRates.json')
		data = json.loads(tax_rates.read()) 
	#
	# pipdata = json.loads(open('taxRates.json').read()) 

	year = data["year"]
	mg_taxRate = data["taxRate"]
	wealth = data["income"]

	data_ln = zip(year, mg_taxRate, wealth)

	#zip together
	def main():
		#query = "INSERT INTO practice_tr (yr, tr, wealth) VALUES ({}, {}, {})"
		query_insert = "INSERT INTO taxRate (yr, mgTaxRate, wealth_amt) VALUES (%s, %s, %s)"

		for yr in data_ln:
			#print(query.format(yr[0], yr[1], yr[2]))
			#data_ln = (yr[0], yr[1], yr[2])
			cursor.execute(query_insert, yr)
			print(cursor.lastrowid, "was inserted")

		
		
		link.commit()

		cursor.close()
		link.close()






	if __name__ == '__main__':
		main()




