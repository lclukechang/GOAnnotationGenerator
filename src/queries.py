#########################################################################
# queries.py
#
# Contains MySQL queries used to retrieve and build GO Term based
# querysets to feed to QueryRunner.
#
# Author: Luke Yulun Chang
# Email: lukechang94@gmail.com
# 
# Bader Lab @ The University of Toronto
##########################################################################

# retrieves all GO Terms with where # of annotated genes >= lower_bound
lower_bound = 10
goterm_sql = """SELECT term.name, term.acc, term.term_type FROM term
 INNER JOIN association ON(term.id=association.term_id)
 INNER JOIN gene_product ON(association.gene_product_id=gene_product.id)
 INNER JOIN species ON(gene_product.species_id=species.id) 
WHERE species.species='sapiens' 
GROUP BY term.name HAVING count(term.name) >= %d;""" % lower_bound

basequery = """SELECT
 gene_product.symbol AS symbol
FROM gene_product
 INNER JOIN association ON (gene_product.id=association.gene_product_id)
 INNER JOIN term ON (association.term_id=term.id)
 INNER JOIN species ON (gene_product.species_id=species.id)
WHERE
 term.name='%s' AND species.species='sapiens';"""

unannotated_genes = """PRAGMA temp_store=2;
create temp table temp2 (node_id int, symbol text);
insert into temp2 (node_id) select distinct (node_id) from degrees where node_id not in (select node_id from gene_annos);

update temp2 set symbol = (select  identifiers.symbol from identifiers where identifiers.node_id = temp2.node_id and identifiers.source = 'Gene Name')  where symbol is null;
update temp2 set symbol = (select identifiers.symbol from identifiers where identifiers.node_id = temp2.node_id and identifiers.source = 'Ensembl Gene Name')  where symbol is null;
update temp2 set symbol = (select identifiers.symbol from identifiers where identifiers.node_id = temp2.node_id and identifiers.source = 'Ensembl Gene ID') where symbol is null;
update temp2 set symbol = (select identifiers.symbol from identifiers where identifiers.node_id = temp2.node_id and identifiers.source = 'Entrez Gene ID') where symbol is null;

.sep "\t"
select symbol, '+', symbol from temp2;
"""
