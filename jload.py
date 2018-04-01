'''
Created on Feb 27, 2018

@author: niuni
'''
import json

infile = open("output.json")

jload = json.load(infile)
infile.close()

print(jload)