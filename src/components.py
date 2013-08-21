#!/usr/local/bin/python

#########################################################################
# querybuilder.py
#
# Builds GeneMANIA query files using GO Terms.
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################
import sys

import numpy as np
from helpers import *
from queries import go_term_sql
from classes import GO_Term
import settings

# Retrieve all query GO terms.
def build_queryfiles():
    terms = execute_sql(goterm_sql)
    term_objs = []
    for term in terms:
        term_obj = GO_Term(term[0], term[1], term[2])
        # Retrieve genes associated with term.
        term_obj.retrieve_queryset(settings, species)
        # Create temporary queryfile.
        term_obj.create_queryfile(settings.cache)
        term_objs.append(term_obj)
    return term_objs
 
# Feed queries into GeneMANIA in cycles.
def run_queries(terms_raw):
    # Split terms into cycles of size n.
    n = pow(int(settings.threads), 3)
    terms = splitarray(terms_raw, n)
    for i in range(len(terms)):
        # Produce querypath list.
        for term in terms[i]:
            paths = [term.querypath]
        print "[Invoking QueryRunner: cycle %d of %d]" % (i, len(terms))
        queryrunner = sh.java('org.genemania.plugin.apps.QueryRunner', 
            '--data', settings.data, '--threads', settings.threads, 
            '--out', 'scores', '--results', settings.scorecache, paths)
        # TODO: logging for queryrunner errors
        # if queryruner.stdout:
            # log.write.....
        # if queryrunner.stderr:
            # log.write.....
        # Delete temporary queryfiles.
        # TODO: log # of query genes before deleting queryfile
        # NOTE: use count.py to do this!
        sh.rm(queries)
        return terms_raw

# Produce annotation predictions by thresholding with arithmetic mean.
def produce_annos(terms):
    predictions = []
    for term in terms:
        try:
            f = open(term.pred_path)
            lines = [line.rstrip() for line in list(f)]
            y = []
            genelst = []
            q_genes = []
            for l in lines:
                if "\t" not in l:
                    q_genes.append(l)
                else:
                    cols = l.split("\t")
                    genelst.append(cols[0])
                    y.append(float(cols[1]))
            # Update term queryset with actual queryset used in computation.
            term.queryset = QuerySet(q_genes)
            y = np.array(y)
            # Compute first differences.
            y1 = np.diff(y)
            threshold = np.mean(y1[y1<0])
            # Perform thresholding on resultant gene list.
            genelst = genelst[:index_threshold(threshold, y1)]
        # TODO: add logging in addition to print messages for errors
        except IOError:
            print "Error opening file %s." % term.pred_path
        except ThresholdError:
            print "No threshold encountered while processing %s,", \
                term.pred_path
        finally:
            f.close()
        for gene in genelst:
            predictions.append(Prediction(term, gene, len(q_genes)))
    return predictions

# Filter favourable predictions by cross-checking intersects with Single
# Gene Queries (Khalid's Method)
def intersect_filter(predictions):
    




    return favourable, remaining

    

