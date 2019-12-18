'''

author Omar Bani-Issa
@omaroo99

'''

import requests
import json 
import argparse
from threading import *	


def sendRequest(url, keywords, fileName=None):
	r = requests.session()
	certsh = "https://crt.sh"

	for key in keywords:
		data = {"q":"%{}%.{}".format(key, url), "output":"json"}
		response = r.post(url = certsh, data= data)
		parseJson(response.text, fileName)	
		 # here should be multi-threading 


def parseJson(response, out=None):
	json_data = json.loads(response)
	for i in range(len(json_data)):
		if out != None:
			writeFile(json_data[i]['name_value'], out)
		else:
			print(json_data[i]['name_value'])		



def writeFile(data, fileName):
	with open (fileName, 'a') as fd:
		fd.write(data+'\n')


def main():
	arparser = argparse.ArgumentParser()

	arparser.add_argument(
	"-u", "--url", required=True, help="Domain to scan"
	)

	arparser.add_argument(
	"-k", "--keywords", required=True, help="Subdomains to scan saperated by comma (e.g) corp,sports"
	)

	arparser.add_argument(
	"-o", "--outputFile", required=False, help="Enter the name of the output file"
	)



	parser = vars(arparser.parse_args())

	domain = parser['url'] 
	subdomains = parser['keywords'].split(",")
	outputFile = parser['outputFile']
	thread = []
	for i in range(len(subdomains)):
		process = Thread(target=sendRequest, args=[domain,subdomains,outputFile])
		process.start()
		thread.append(process)
	for p in thread:
		p.join()

if __name__ == '__main__':
	main()
