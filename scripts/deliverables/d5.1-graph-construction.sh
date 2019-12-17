#!/bin/sh

# in case an argument is provided is used as the uri
URI=${1:-"mongodb://localhost:27017/"}
echo "connecting to ipc database hosted at: ${URI}"

# ingest entities from resources (genes and proteins)
echo "generate entities for genes and proteins from resources"
ipcrg-entities-from-resources -u ${URI} -d ipc
# KEGG drugs
echo "parse KEGG drugs from BSC"
ipcrg-parse-edge-list -f data/KEGG_drugs.19-10-2019.gr -u ${URI} -d ipc --source_entity gene --relation drug
# BioGrid
echo "parse BioGRID from BSC"
ipcrg-parse-edge-list -f data/BioGRID_interactions.19-10-2019.gr -u ${URI} -d ipc --source_entity gene --relation biogrid
# MONDO
echo "parse MONDO from BSC"
ipcrg-parse-edge-list -f data/MoNDO_diseases.19-10-2019.gr -u ${URI} -d ipc --source_entity gene --relation mondo
# Reactome
echo "parse Reactome from BSC"
ipcrg-parse-edge-list -f data/Reactome_pathways.19-10-2019.gr -u ${URI} -d ipc --source_entity gene --relation reactome
# Recon3D metabolite
echo "parse Recon3D metabolite from BSC"
ipcrg-parse-edge-list -f data/Recon3D_metabolites.19-10-2019.gr -u ${URI} -d ipc --source_entity gene --relation recon3d-metabolite
# Curie
echo "parse multi-layer network from Curie"
ipcrg-parse-edge-list -f data/multi.layer.net.gr -u ${URI} -d ipc --source_entity patient --target_entity gene --relation curie
# create indexes
echo "create indexes"
ipcrg-create-indexes -u ${URI} -d ipc
