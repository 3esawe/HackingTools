'''

author Omar Bani-Issa
@omaroo99

'''

import requests
import json 
import argparse
from threading import *	
from multiprocessing.dummy import Pool as ThreadPool

arparser = argparse.ArgumentParser()

arparser.add_argument(
"-u", "--url", required=True, help="Domain to scan"
)

arparser.add_argument(
"-k", "--keywords", required=False, help="Subdomains to scan saperated by comma (e.g) corp,sports"
)

arparser.add_argument(
"-o", "--outputFile", required=False, help="Enter the name of the output file"
)

arparser.add_argument(
"-i", "--inputFile", required=False, help="Enter the name of the input file to get the subdomains from"
)


arparser.add_argument(
"-t", "--threads", required=False, help="Enter the number of threads"
)


parser = vars(arparser.parse_args())
threadNum = 5
domain = parser['url'] 
subdomains = parser['keywords']
outputFile = parser['outputFile']
inputFile = parser['inputFile']


if parser['threads'] != None:
	threadNum = parser['threads'] 

# def sendRequest1(url, keywords, fileName=None):
# 	r = requests.session()
# 	certsh = "https://crt.sh"

# 	for key in keywords:
# 		# print(key)
# 		data = {"q":"%.{}.{}".format(key, url), "output":"json"}
# 		response = r.post(url = certsh, data= data)
# 		parseJson(response.text, fileName)	
# 		 # here should be multi-threading 

def sendRequest(key):
	r = requests.session()
	certsh = "https://crt.sh"
	data = {"q":"%.{}.{}".format(key, domain), "output":"json"}
	response = r.post(url = certsh, data= data)
	parseJson(response.text, outputFile)	


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

def parseFile(inFile):
	with open (inFile, 'r') as handle:
		inList = handle.readlines()
	inList = [x.strip() for x in inList]
	# print(inList)
	return inList

def main():


	global inputFile


	if inputFile != None:
		# inputFile = parseFile(inputFile)
		# # print(inputFile)
		# thread = []
		# for i in range(int(threadNum)):
		# 	process = Thread(target=sendRequest, args=[domain,inputFile,outputFile])
		# 	process.start()
		# 	thread.append(process)
		# for p in thread:
		# 	p.join()

		inputFile = parseFile(inputFile)
		pool = ThreadPool(int(threadNum))
		results = pool.map(sendRequest, inputFile)

	else:
		# thread = []
		# for i in range(len(subdomains.split(','))):
		# 	process = Thread(target=sendRequest, args=[domain,subdomains,outputFile])
		# 	process.start()
		# 	thread.append(process)
		# for p in thread:
		# 	p.join()
		inputFile = subdomains.split(',')
		pool = ThreadPool(int(threadNum))
		results = pool.map(sendRequest, inputFile)


if __name__ == '__main__':
	main()
