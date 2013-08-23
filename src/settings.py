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
jar = "/Users/lukechang/dev/dependencies/cmd.jar"

# Path to a GeneMANIA network dataset to use for predictions
data = "/Users/lukechang/dev/dependencies/datasource"

# Amount of memory to allocate JVM when executing GeneMANIA tools
mem = "-Xmx2500m"

# For multi-core systems, set to maximum number of physical cores
threads = "2"

# Provide a path to store intermediate query files during runtime
querycache = "/Users/lukechang/dev/GOAnnotationGenerator/.querycache"

# Provide a path to store intermediate score files during runtime
# NOTE: This cannot be identical to the querycache path!
scorecache = "/Users/lukechang/dev/GOAnnotationGenerator/.scorecache"

# Provide a path to store log files
log = "/Users/lukechang/dev/GOAnnotationGenerator/log"

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
summary_path = "/Users/lukechang/dev/dependencies/summary.sqlite"

# Provide the path to a GeneOntology obo-xml.gz file.
go_file = "/Users/lukechang/dev/dependencies/go_daily-termdb.obo-xml.gz"

# Provide the path to a AnnotationCorpus for Humans.
ac_file = "/Users/lukechang/dev/dependencies/gene_association.goa_human"

# Set weights for confidence scores
semsim_weight = 0.15
crossval_weight = 0.85
