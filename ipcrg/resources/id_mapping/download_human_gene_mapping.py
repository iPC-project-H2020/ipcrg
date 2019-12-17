"""Download the latest NCBI id mapping for humans."""
import os
import argparse
import urllib.request
import pandas as pd

MAPPING_FTP_FILEPATH = (
    'ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/'
    'gene2accession.gz'
)
TAX_ID = 9606

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
    urllib.request.urlretrieve(MAPPING_FTP_FILEPATH, args.filepath)
    # extract specific taxonomy data
    mapping_df = pd.concat(
        [
            batch[batch.index == TAX_ID] for batch in
            pd.read_csv(args.filepath, sep='\t', index_col=0, chunksize=10000)
        ],
        sort=False
    )
    # delete the full file
    os.remove(args.filepath)
    # dump the mapping file
    mapping_df.to_csv(args.filepath, sep='\t')
