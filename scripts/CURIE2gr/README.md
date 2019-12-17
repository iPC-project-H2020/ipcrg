# Medulloblastoma data-driven network identifiers conversion

## Motivation

To harmonize the identifiers used in the relational graph databse, we converted the node labels of the data-driven network provided by CURIE to Entrez idenifiers. The converted data-driven network was then ingested into the relational graph database, excluding the gene-gene interaction (GGI) sub-graph as it contains only those genes present in at least one of data-driven network input data-sets. All scripts and generated files are placed in the directory `scripts/CURIE2gr`.

## Retrieve the edge list of CURIE data-driven network

We downloaded the archive `MultilayerNetwork.RData` from a shared [Google Drive directory](https://drive.google.com/drive/folders/1goXgmO3WyYysgJxmErsNYZe2_ykfNWPV?usp=sharing). Within R statical environment (version 3.6.1), we generated the file `multi.layer.net`: 

```R
load('MultilayerNetwork.RData')
write.table(multi.layer.net,'multi.layer.net',sep='\t',row.names=F,quote=F)
```

The file consists of an edge list composed of 35587 nodes of two types (patients and genes) and 699025 edges with 4 attributes describing the input data-sets ('Methylation','Phospho','Protein','RNAseq'). After the conversion to Entrez identifiers, the number of unique nodes is slightly reduced (see Results).

## Identifier conversion

The script `CURIE2gr.py` (Python 3.7.3) automatically converts the node entry labels (UniProt, Swiss-Prot, RefSeq identifiers, and default and unofficial gene symbols) in the input file `multi.layer.net` to Entrez identifiers. The edgelist of the data-driven network with converted labels is reported in the output file `multi.layer.net.gr`. Labels that cannot be converted are kept in their original form. The file `multi.layer.net.vocab` is a look-up table that map the original labels to the converted ones.

```python
python scripts/CURIE2gr.py
```

As for nodes displaying **Phospho** and **Protein** edge attributes, UniProt identifiers were converted in batch to Entrez identifiers by querying [UniProt database mapping service](https://www.uniprot.org/help/api_idmapping), after adding the '_HUMAN' sufix if missing. Entrez identifiers of the unmapped entries were retrieved individually via [Uniprot programmatic access](https://www.uniprot.org/help/api_retrieve_entries).

As for nodes displaying **Methylation** and **RNAseq** edge attributes, the script `extract_Hsap.pl` is called to parse files from [NCBI FTP site](ftp://ftp.ncbi.nih.gov/gene/DATA/README) and extract mapping information for human genes. First, the script downloads the file `gene2accession.gz` and generates the file `gene2accession_Hsap`, a comprehensive report of the accessions that are related to human Entrez identifiers ('GeneID'), including Swiss-Prot and RefSeq. The unmapped entries are then searched in the downloaded file `gene_info.gz`, mapping default (_Symbol_) and unofficial symbols for human genes (_Synonyms_) to unique Entrez identifier (_GeneID_). The remainig unmapped entries are finally queryied via mygene (version 3.1.0), a Python wrapper to access MyGene.Info, a REST web service to query gene annotation data.

## Results

2.8% (1020/35549) unmapped entries are reported with the original labels. 19 of them are obsolete UniProt entries, while the others are clone-based annotations, novel/putative/uncharacterized gene products, pseudogenes, mitochondrial transcripts.
