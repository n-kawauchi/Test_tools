#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def output():
	for item in r.json():
		if item["tag_name"] == "v1.2.1":
			print("tag_name: ",item["tag_name"])
			for n in range(len(item["assets"])):
				print(item["assets"][n]["name"])
				print("download count: ", item["assets"][n]["download_count"])
				print("")

r = requests.get('https://api.github.com/repos/OpenRTM/OpenRTM-aist/releases')
output()

r = requests.get('https://api.github.com/repos/OpenRTM/OpenRTM-aist-Python/releases')
output()

r = requests.get('https://api.github.com/repos/OpenRTM/OpenRTM-aist-Java/releases')
output()
