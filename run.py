#!/usr/local/bin/python

#########################################################################
# termpredictor.py
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
import sh
import time
import datetime
import os

import settings

# generate querysets

# run queries in QueryRunner

# threshold results

# produce composite confidence scores and filter
