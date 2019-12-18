#!/usr/bin/python

'''



Description : This script will help you in HackTheBox, vulnhub ..
by searching for important keywords in HTML source code

'''
from tabulate import tabulate
import requests 
from bs4 import BeautifulSoup
import re
import sys
import optparse


links = []
script_links = []
img_src = []
script_content = []

def source(url):
	if "http://" not in url and "https://" not in url:
		print("[+] You forgot to enter http:// or https://")
	req = requests.get(url)
	return req.text


def anlayzer(source_code, keywrods):
	# print(source_code)
	soap =	BeautifulSoup(source_code,features="lxml")
	for key in keywrods:
		# links.append([a for a in soap.findall('a', {"href":True})])
		# script_links.append([s for s in soap.findall('script', {'src':True})])
		# img_src.append([m for m in soap.findall('img',{'src':True})])
		if key == 'a':
			tag = soap.a
			links.append([a['href'] for a in soap.find_all('a', {"href":True})])
		if key == 'script' :
			tag = soap.script
			# src = tag['src']
			content = soap.script.string
			script_links.append([s['src'] for s in soap.find_all('script', {'src':True})])
			script_content.append(content)
		if key == 'img':
			tag = soap.img
			if tag != None:
				script_links.append([s['src'] for s in soap.find_all('script', {'src':True})])


def main():
	parser = optparse.OptionParser('[+] usage -u <target url> -k <path for keywrods> -f <keywrods file>')
	parser.add_option('-u', dest='traget_url', type='string',help='[+] Enter target url')
	parser.add_option('-k', dest='keywrods', type='string',help='[+] Enter target keywrods saprated by comma')
	parser.add_option('-f', dest='file', type='string', help='[+] Enter the path for keywrods file')
	(options, args) = parser.parse_args()
	


	url = options.traget_url
	keywrods = options.keywrods.split(',')
	file = options.file


	if keywrods == None and file == None:
		print(parser.usage)

	elif keywrods != None and file == None:
		source_code = source(url)
		anlayzer(source_code, keywrods)
	else:
		source_code = source(url)
		anlayzer(source_code, file)

	table = [links,img_src,script_links]
	print(tabulate(table,headers=['links', 'img src', 'script_links']))
if __name__ == '__main__':
	main()