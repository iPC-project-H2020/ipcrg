"""Core I/O module."""
import pkg_resources
import pandas as pd
from functools import lru_cache


def parse_edge_list(filepath, **kwargs):
    """
    Parse edge list.

    Args:
        filepath (str): path to the file.
        kwargs (dict): key-value arguments for pd.read_csv.

    Returns:
        typing.Tuple[pd.DataFrame, typing.List[str], typing.List[str]]:
            dataframe, entity labels and relation labels.
    """
    # TODO: add parser for cytoscape (xlmmgs files)
    if filepath.endswith('.gr'):
        df = pd.read_csv(filepath, sep='\s+').dropna(how='any', axis=0)
    else:
        df = pd.read_csv(filepath, **kwargs).dropna(how='any', axis=0)

    source_entity_labels = sorted(list(set(df.values[:, 0])))
    target_entity_labels = sorted(list(set(df.values[:, 1])))

    if df.shape[1] == 2:
        columns = ['source', 'target']
    elif df.shape[1] == 3:
        columns = ['source', 'target', 'subtype']
    elif df.shape[1] == 4:
        columns = ['source', 'target', 'subtype', 'weight']
    else:
        raise RuntimeError(
            'Unexpected number of columns: {} \n'.format(df.shape[1]) +
            'Supported configurations are:\n' +
            '- 2 columns, entities only\n' +
            '- 3 columns, entities and relation subtype\n' +
            '- 4 columns, entities, relation subtype and weights\n'
        )
    df.columns = columns
    return df, source_entity_labels, target_entity_labels


@lru_cache(maxsize=None)
def get_gene_id_mapping_df():
    """
    Get dataframe representing the id mapping for genes.
    The function cache the results to prevent unnecessary calculations.

    Returns:
        pd.DataFrame: dataframe for id mapping.
    """
    filepath = pkg_resources.resource_filename(
        'ipcrg', 'resources/id_mapping/gene.tsv.gz'
    )
    data = pd.read_csv(filepath, sep='\t')
    return data[['GeneID', 'Symbol']].drop_duplicates().reset_index(drop=True)


@lru_cache(maxsize=None)
def get_protein_id_mapping_df():
    """
    Get dataframe representing the id mapping for proteins.
    The function cache the results to prevent unnecessary calculations.

    Returns:
        pd.DataFrame: dataframe for id mapping.
    """
    filepath = pkg_resources.resource_filename(
        'ipcrg', 'resources/id_mapping/protein.tsv.gz'
    )
    data = pd.read_csv(filepath, sep='\t')
    return data[['UniProtKB-AC', 'GeneID', 'Gene_Name',
                 'Gene_Synonym']].drop_duplicates().reset_index(drop=True)
