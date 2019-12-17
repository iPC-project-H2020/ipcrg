"""Download the latest UniProt id mapping for humans."""
import os
import argparse
import urllib.request
import pandas as pd

CURRENT_RELEASE_MAPPING_FTP_FILEPATH = (
    'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/'
    'knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping.dat.gz'
)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-o',
    '--filepath',
    type=str,
    help='path where to store the file.',
    required=True
)

if __name__ == '__main__':
    # parse arguments
    args = parser.parse_args()
    # download the file
    urllib.request.urlretrieve(
        CURRENT_RELEASE_MAPPING_FTP_FILEPATH, args.filepath
    )
    # extract specific ids of interest and create mapping file
    mapping_df = pd.read_csv(
        args.filepath, sep='\t', names=['UniProtKB-AC', 'id_type', 'id_value']
    )
    mapping_df = mapping_df[mapping_df['id_type'].str.match(
        r'GeneID|Gene_Synonym|Gene_Name'
    )].pivot_table(
        index='UniProtKB-AC',
        columns='id_type',
        values='id_value',
        aggfunc=lambda a_list: ';'.join(a_list)
    ).reset_index()
    # delete the full file
    os.remove(args.filepath)
    # dump the mapping file
    mapping_df.to_csv(args.filepath, sep='\t', index=None)
