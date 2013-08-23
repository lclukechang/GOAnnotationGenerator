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
# Add debug message
import os

import sh
import pandas as pd
import numpy as np
from fastSemSim.GO import AnnotationCorpus
from fastSemSim.GO import GeneOntology
from fastSemSim.SemSim import SemSimMeasures

import settings
from helpers import *
from queries import goterm_sql, unannotated_genes
from classes import *

# Retrieve all query GO terms.
def build_queryfiles():
    terms = execute_sql(goterm_sql)
    term_objs = []
    print "[Building queryfiles...]"
    for term in terms:
        term_obj = GO_Term(term[0], term[1], term[2])
        # Retrieve genes associated with term.
        term_obj.retrieve_queryset()
        # Create temporary queryfile.
        term_obj.create_queryfile(settings.querycache)
        term_objs.append(term_obj)
    return term_objs

# Threshold and filter out querysets with low predictive values as
# determined by cross-validation.
def queryset_threshold(term_objs):
    # Build cross-validation queryfile.
    querypath = os.path.join(settings.querycache, "crossval.query")
    f = open(querypath, "w")
    for term in term_objs:
        f.write("%s\t+\t%s\n" % 
            (term.name, "\t".join(term.queryset.members)))
    f.close()
    
    # Run cross-validation.
    print ["Running queryset validation..."]
    resultpath = os.path.join(settings.scorecache, "crossval.csv")
    javacmd("org.genemania.plugin.apps.CrossValidator", "--data",
        settings.data, "--threads", settings.threads, "--organism",
        "H. Sapiens", "--query", querypath, "--networks",
        settings.networks, "--folds", settings.folds, "--outfile",
        resultpath, "--method", "automatic")
    print ["Applying Cross-Validation Queryset Predictive Value filter..."]
    dat = pd.read_csv(resultpath, 
        usecols = ["queryIdentifier", "fold #", "AUC-ROC"], 
        sep = "\t")
    sh.rm(resultpath)
    dat = dat[dat["fold #"] == "-"][["queryIdentifier", "AUC-ROC"]]
    descending = dat.sort(columns = "AUC-ROC", ascending = False)
    mean = descending[["AUC-ROC"]].mean().loc["AUC-ROC"]

    # Retain those querysets which have predictive value higher than
    # arithmetic mean of all AUC-ROC scores from cross-validation.
    screen = descending[descending["AUC-ROC"] > mean]
    d = {}
    for i, row in screen.iterrows():
        d[row["queryIdentifier"]] = row["AUC-ROC"]

    # Filter query GO terms, retaining sets with high AUC-ROC scores.
    filtered = []
    for term in term_objs:
        try:
            term.pred_value = d[term.name]
            filtered.append(term)
        except KeyError:
            continue
    return filtered
 
# Feed queries into GeneMANIA in cycles.
def run_queries(term_objs):
    # Split terms into cycles of size n.
    n = pow(int(settings.threads), 3)
    terms = splitarray(term_objs, n)
    for i in range(len(terms)):
        # Produce querypath list.
        paths = [term.querypath for term in terms[i]]
        print "[Invoking QueryRunner: cycle %d of %d]" % (i, len(terms))
        queryrunner = javacmd('org.genemania.plugin.apps.QueryRunner', 
            '--data', settings.data, '--threads', settings.threads, 
            '--out', 'scores', '--results', settings.scorecache, paths)
        # TODO: logging for queryrunner errors
        # if queryruner.stdout:
            # log.write.....
        # if queryrunner.stderr:
            # log.write.....
        # Delete temporary queryfiles.
        sh.rm(paths)

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
            for gene in genelst:
                predictions.append(Prediction(term, gene, len(q_genes)))
        # TODO: add logging in addition to print messages for errors
        except IOError:
            print "Error opening file %s." % term.pred_path
        except ThresholdError:
            print "No threshold encountered while processing %s,", \
                term.pred_path
        finally:
            f.close()
    return predictions

# Filter favourable predictions by cross-checking intersects with Single
# Gene Queries (Khalid's Method)
def intersect_filter(predictions):
    # Query GeneMANIA summary sqlite to retrieve unannotated genes
    ret = sh.sqlite3(settings.summary_path, _in = unannotated_genes)
    querypath = os.path.join(settings.querycache, "unknown_genes.query")
    f = open(querypath, "w")
    f.write(ret.stdount)
    f.close()

    # Compute single gene predictions.
    print "[Computing functional enrichment predictions for \
            cross-checking and filtering...]"
    resultpath = os.path.join(settings.querycache, "func_enrich_results")
    sh.java(settings.mem, "-cp", 
        "functional_enrichment/engine-progs-1.1.0.jar:%s" % settings.jar,
        "org.genemania.engine.sandbox.apps.FunctionPredictor", 
        "-indexDir", settings.data, "-cachedir",
        os.path.join(settings.data, "cache"), "-qfile", querypath,
        "-orgid", "4", "-method", "BP", "-out", resultpath,
        "-netids", "all", "numrelated", "20", "-log",
        os.path.join(settings.log, "func_enrich_log.txt"))
    sh.rm(querypath)

    # Load functional enrichment predictions as dictionary and filter.
    screen = import_func_preds(resultpath)
    favourable, semsim, remaining = [], [], []
    for pred in predictions:
        try:
            sing_pred = screen[pred.gene]
            if sing_pred is pred.term.acc:
                pred.score = "cross-predicted"
                favourable.append(pred)
            else:
                semsim.append((pred, sing_pred))
                remaining.append(pred)
        except KeyError:
            remaining.append(pred)
    return favourable, semsim, remaining

# Compute semantic-similarity scores for applicable predictions.
def semsim_score(pairs):
    try:
        go = GeneOntology.load_GO_XML(go_file)
    except:
        print "Error Loading ontologies from %s" % go_file
    try:
        ac = AnnotationCorpus.AnnotationCorpus(go)
        ac.parse(ac_file, "GOA")
        ac.sanitize()
    except:
        print "Error Loading annotations from %s" % ac_file

    TermSemSimClass = SemSimMeasures.selectTermSemSim("Resnik")
    TSS = TermSemSimClass(ac,go)
    TSS.setSanityCheck(True)
    scored = []
    det_max = []
    for pred, sing_pred in pairs:
            pred.score = (TSS.SemSim(pred.term.acc, sing_pred) * 
                settings.semsim_weight)
            scored.append(pred)
            det_max.append(pred.score)
    # Normalize semsim scores
    maxscore = np.max(np.array(det_max))
    for pred in scored:
        pred.score /= maxscore
    return scored

# Compute weighted confidence scores.
def weight_scores(semsim_scored, rem):
    weighted = []
    for pred in semsim_scored:
        pred.score += pred.term.pred_value * settings.crossval_weight
        weighted.append(pred)
    for pred in rem:
        pred.score = pred.term.pred_value * settings.crossval_weight
        weighted.append(pred)
    return weighted
    
def output_annos_log_form(final_preds):
    f = open("./test", "w")
    f.write("Gene\tGO:ACC\tName\tConfidence Score\n")
    for pred in final_preds:
        f.write("%s\t%s\t%s\t%s\n" % 
                (pred.gene, pred.term.acc, pred.term.name, pred.score))
    f.close()



