#########################################################################
# helpers.py
#
# Helper functions for GOAnnotationGenerator.
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################
import string
import time

import sh
import MySQLdb
import httplib2
import json

import settings

# Bake "sh" java to reduce redundancy.
javacmd = sh.java.bake(settings.mem, '-cp', settings.jar)

# Connects to and executes a query into AMIGO db.
def execute_sql(query):
    db = MySQLdb.connect(user = "root", db = "GO")
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows

# Strips content from a list/tuple of unary tuples.
def strip_unary_tuple(t):
	t = map(lambda x: x[0],t)
	return t

# Handles output from GeneMANIA command line tool: GeneSanitizer. 
# Splits sanitized list into 2 lists (query, missing).
def sanitizer_handler(sanitizedlist):
	query, missing = [], []
	for l in sanitizedlist.splitlines()[1:]:
		#strip trailing tabs
		line = l.rstrip('\t')
		if "\t" not in line.rstrip('\t'):
			missing += [line]
		else:
			words = string.split(line,"\t",1)
			query += [words[1]]
	return query, missing

# Sanitizes and handles sanitized output by splitting into genes 
# recognized and unrecognized by GeneMANIA.
def sanitize_split(unsanitized):
	str_input = '\n'.join(unsanitized)
	sanitizer_ret = javacmd(
	'org.genemania.plugin.apps.GeneSanitizer', '--data', settings.data,
	'--organism', "H. Sapiens", _in=str_input)
	sanitized = sanitizer_ret.stdout
	return sanitizer_handler(sanitized)

# Takes a list of genes, removes duplicates, maps to Ensembl Gene IDs.
#TODO: add return value with list of skipped genes (that could not be mapped to Ensembl Gene IDs)
def ensemblmapper(symbols, species):
	errors=[]
	if not symbols:
		return []
	else:
		ids = []
		#prime Ensembl REST API request
		server = "http://beta.rest.ensembl.org"
		#TODO: error checking for cache creation
		http = httplib2.Http(".cache")
		for symbol in symbols:
			#restrict query to only return genes
			request = "/xrefs/symbol/%s/%s?object=gene" %(species,symbol)
			response, content = http.request(server+request, method="GET",
				headers={"Content-Type":"application/json"})
			if not response.status == 200:
				errors += ["Invalid response from API (EnsemblMapper): %s with symbol %s." % (response.status, symbol)]
				continue
			# Assumes first gene in response is correct.
			decoded = json.loads(content)
			if decoded:
				ids += [decoded[0]['id']]
			time.sleep(0.34)
		return list(set(ids)), errors

# Returns generator that returns chunks of array size n.
def splitarray(array, n):
	out = []
	l = len(array)
	for i in range(0,l,n):
		if i+n > l:
			out.append(array[i:l])
		else:
			out.append(array[i:(i+n)])
	return out

# Takes a threshold value and returns cutoff index.
def index_threshold(threshold, array):
	for tup in enumerate(array):
		if threshold < tup[1]:
			return tup[0]
		elif tup[0] == len(array) - 1:
			raise ThresholdError

# Imports functional enrichment results as dictionary.
def import_func_preds(path):
	f = open(path)
	lines = list(f)
	f.close()
	d = {}
	for l in lines:
		cols = l.rstrip().split()
		if cols[1] is not "null":
			d[cols[0]] = cols[1]
	return d

class ThresholdError(Exception):
	pass
