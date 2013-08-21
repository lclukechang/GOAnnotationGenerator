#########################################################################
# classes.py
#
# Definitions for classes.
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################
import sys
import os

from helpers import *
from queries import basequery
from settings import *

class GO_Term:
    def __init__(self, name, acc, branch):
        self.name = name
        self.sql_name = name.replace("\'", "\'\'")
        self.file_name = name.replace(" ", "_").replace("/", "OR")
        self.acc = acc
        self.branch = branch

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.name

    def retrieve_queryset(self, species):
        queries = execute_sql(basequery % (self.sql_name, "sapiens"))
        self.queryset = QuerySet(queries)
        self.queryset.sanitize()

    def create_queryfile(cachepath):
        self.querypath = os.path.join(cachepath, "%s.query" % 
            self.file_name)
        f = open(querypath, 'w')
        content = ["H. Sapiens", self.queryset.string(), networks, '100',
            weighting]
        f.write("\n".join(content))
        f.close()
        self.pred_path = self.querypath + "-results.scores.txt"

class QuerySet:
    def __init__(self, members):
        self.members = list(set(members))
        self.sanitation = False

    def sanitize(self):
        if not self.sanitation:
            sanitized, unrecognized = sanitize_split(self.queryset)
            #TODO: log errors
            converted, errors = ensemblmapper(unrecognized, 
                "homo_sapiens")
            self.queryset = sanitized + converted
            self.sanitation = True

class Prediction:
    def __init__(self, term, gene, count):
        self.term = term
        self.gene = gene
        self.querycount = count
        # Init confidence score to be none
        self.ci = None


