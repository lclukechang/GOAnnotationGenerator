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
        self.pred_value = None
        self.queryset = None
        self.querypath = None
        self.pred_path = None

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.name

    def retrieve_queryset(self):
        queries = execute_sql(basequery % self.sql_name)
        self.queryset = QuerySet(queries)
        self.queryset.sanitize()

    def create_queryfile(self, cachepath):
        self.querypath = os.path.join(cachepath, "%s.query" % 
            self.file_name)
        f = open(self.querypath, 'w')
        content = ["H. Sapiens", "\t".join(self.queryset.members), 
            networks, '100', weighting]
        f.write("\n".join(content))
        f.close()
        self.pred_path = "%s.query-results.scores.txt" % os.path.join(scorecache, self.file_name)

class QuerySet:
    def __init__(self, members):
        self.members = list(set(strip_unary_tuple(members)))
        self.sanitation = False

    def sanitize(self):
        if not self.sanitation:
            sanitized, unrecognized = sanitize_split(self.members)
            #TODO: log errors
            if unrecognized:
                converted, errors = ensemblmapper(unrecognized, 
                    "homo_sapiens")
                self.members = sanitized + converted 
            self.sanitation = True

class Prediction:
    def __init__(self, term, gene, count):
        self.term = term
        self.gene = gene
        self.querycount = count
        # Init confidence score to be none.
        self.score = None