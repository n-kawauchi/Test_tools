#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
from requests.auth import HTTPBasicAuth
import argparse

LATEST_RELEASE = "v1.2.1"
BRANCH = "svn/RELENG_1_2"
BRANCH_RTP = "RELENG_1_2"
GITHUB_OWNER = "OpenRTM"

p = argparse.ArgumentParser()
p.add_argument('repository', help='GitHub Repository [Example: OpenRTM-aist]')
p.add_argument('username', help='GitHub user name')
p.add_argument('password', help='GitHub user password')
args = p.parse_args()

def get_hash_of_latest_release(reporitory, username, password):
	url = "https://api.github.com/repos/" + GITHUB_OWNER + "/" + reporitory + "/tags"
	r = requests.get(url, auth=HTTPBasicAuth(username, password))
	
	for item in r.json():
		if item["name"] == LATEST_RELEASE:
			sha = item["commit"]["sha"]
			print("Tag name: ",item["name"])
			#print("Tag sha: ",sha)

	return sha

def get_PR_number_of_latest_release(repository, username, password, sha):
	url = "https://api.github.com/repos/" + GITHUB_OWNER + "/" + repository + "/commits/" + sha
	r = requests.get(url, auth=HTTPBasicAuth(username, password))

	item = r.json()
	if item["sha"] == sha:
		msg = item["commit"]["message"]
		number_s = msg.find("#")
		number_e = msg.find(" ", number_s)
		s = int(number_s)
		e = int(number_e)
		PR_number = msg[s+1:e]
		print("Tag PR_number: ", PR_number)
		print("")
		string = "#{0}以降、{1}へマージされたPR".format(PR_number, BRANCH)
		print(string)
		print("-----")

		return int(PR_number)

def	get_merged_PR_list(repository, username, password, number):
	page = 1
	PR_list = []
	loopend = "false"


	while len(PR_list) > 0 or page == 1: 
		url = "https://api.github.com/repos/" + GITHUB_OWNER + "/" + repository + "/pulls?state=closed&page=" + str(page)
		r = requests.get(url, auth=HTTPBasicAuth(username, password))
		for item in r.json():
			if item["base"]["ref"] == BRANCH:
				if int(item["number"]) > int(number):
					#print("number: ", item["number"])
					#print(item["title"])
					#print(item["user"]["login"])
					data = "{title} (#{num}|{name})".format(title=item["title"], num=item["number"], name=item["user"]["login"]) 
					#print(data)
					PR_list.append(data)
				else:
					loopend = "true"
					break
			else:
				continue
	
		if loopend == "false":
			page += 1
			#print("page: ",page)
			if page > 10:
				print('Abnormal number of attempts.')
				break
		else:
			break

	return(PR_list)

def output(PR_list):
	for item in reversed(PR_list):
		print(item)

if __name__ == '__main__':
	args = sys.argv
	if len(args) > 3:
		repository = args[1]
		username = args[2]
		password = args[3]
		print("Repository: ", GITHUB_OWNER,"/",repository)
		if repository == "OpenRTP-aist":
			BRANCH = BRANCH_RTP
		
	sha = get_hash_of_latest_release(repository, username, password)
	number = get_PR_number_of_latest_release(repository, username, password, sha)
	PR_list = get_merged_PR_list(repository, username, password, number)
	output(PR_list)

