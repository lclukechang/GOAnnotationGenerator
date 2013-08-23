#!/usr/local/bin/python

#########################################################################
# run.py
#
# Generates Gene Ontology Term Annotations by querying GeneMANIA with
# querysets built from all genes associated with a given term. The 
# predictions are thresholded accordingly and filtered according to
# a composite confidence score generated via queryset cross-validation
# and semantic similarity comparisons with results from Khalid Zuberi's
# single-gene "FunctionPredictor".
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################

import argparse
import time
import datetime
import sys

try:
    import fastSemSim
except ImportError:
    print ["Please make sure the fastSemSim library is installed."]
    sys.exit()

from components import *

# TODO: add timing 
# generate querysets
term_objs = build_queryfiles()
filtered_by_crossval = queryset_threshold(term_objs)
run_queries(filtered_by_crossval)
unfiltered_preds = produce_annos(filtered_by_crossval)
fav, semsim_input, rem = intersect_filter(unfiltered_preds)
semsim_scored = semsim_score(semsim_input)
final_preds = weight_scores(semsim_scored, rem)
output_annos_log_form(final_preds)


# run queries in QueryRunner

# threshold results

# produce composite confidence scores and filter
