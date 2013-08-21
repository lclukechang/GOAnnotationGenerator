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

# Path to the GeneMANIA JVM JAR file (command-line tools)
jar = "/Users/lukechang/dev/dependencies/cmd.jar"

# Path to a GeneMANIA network dataset to use for predictions
data = "/Users/lukechang/dev/dependencies/datasource"

# Amount of memory to allocate JVM when executing GeneMANIA tools
mem = "-Xmx2500m"

# For multi-core systems, set to maximum number of physical cores
threads = "2"

# Provide a path to store intermediate query files during runtime
querycache = "~/Users/lukechang/dev/GOAnnotationGenerator/.querycache"

# Provide a path to store intermediate score files during runtime
scorecache = "~/Users/lukechang/dev/GOAnnotationGenerator/.scorecache"

# Provide names of networks to use when querying GeneMANIA
# Refer to http://pages.genemania.org/tools/#available-networks for 
# available networks.
networks = "default"

# Provide weighting method to use when querying GeneMANIA
weighting = "automatic"

