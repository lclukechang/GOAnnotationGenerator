##########################################################################
# settings.py
#
# Settings for GOAnnotationGenerator. Modify settings for usage on local
# machine/architectures, amending paths for local use.
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################

    ##
    # NOTE: Please use ABSOLUTE paths in this settings file!
   ##

# Path to the GeneMANIA JVM JAR file (command-line tools)
jar = "/Users/luke/dev/projects/baderlab/dependencies/cmd.jar"

# Path to a GeneMANIA network dataset to use for predictions
data = "/Users/luke/dev/projects/baderlab/dependencies/datasource"

# Amount of memory to allocate JVM when executing GeneMANIA tools
mem = "-Xmx4000m"

# For multi-core systems, set to maximum number of physical cores
threads = "8"

# Provide a path to store intermediate query files during runtime
querycache = "/Users/luke/dev/projects/baderlab/GOAnnotationGenerator/.querycache"

# Provide a path to store intermediate score files during runtime
# NOTE: This cannot be identical to the querycache path!
scorecache = "/Users/luke/dev/projects/baderlab/GOAnnotationGenerator/.scorecache"

# Provide a path to store log files
log = "/Users/luke/dev/projects/baderlab/OAnnotationGenerator/log"

# Provide names of networks to use when querying GeneMANIA
# Refer to http://pages.genemania.org/tools/#available-networks for 
# available networks.
networks = "default"

# Provide weighting method to use when querying GeneMANIA
weighting = "automatic"

# Number of k-folds to perform when cross-validating querysets.
# NOTE: when adjusting this make sure to adjust lower_bound for querysets
# accordingly to make sure enough data is held back for validation.
folds = "5"

# Provide the path to the sqlite summary used to generate GeneMANIA stats
summary_path = "/Users/luke/dev/projects/baderlab/dependencies/summary.sqlite"

# Provide the path to results from functional enrichment predictions for
# unannotated genes
sing_preds_path =
"/Users/luke/dev/projects/baderlab/GOAnnotationGenerator/src/functional_enrichment/20related_nospd_nonondefaultpredict.txt"

# Provide the path to a GeneOntology obo-xml.gz file.
go_file = "/Users/luke/dev/projects/baderlab/dependencies/go_daily-termdb.obo-xml.gz"

# Provide the path to a AnnotationCorpus for Humans.
ac_file = "/Users/luke/dev/projects/baderlab/dependencies/gene_association.goa_human"

# Set weights for confidence scores
semsim_weight = 0.15
crossval_weight = 0.85
