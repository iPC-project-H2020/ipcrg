"""Building a relational graph for genes using KEGG drugs with MongoDB backend."""  # noqa
import argparse
import matplotlib.pyplot as plt
from ipcrg.interfaces.mongo import MongoDBInterface
from ipcrg.entities.gene import Gene
from ipcrg.relations.drug import Drug

parser = argparse.ArgumentParser()
parser.add_argument(
    '-f', '--filepath', type=str, help='path to the edge list.', required=True
)
parser.add_argument(
    '-u',
    '--uri',
    type=str,
    default='mongodb://localhost:27017/',
    help='uri connection string. Defaults to "mongodb://localhost:27017/".'
)
parser.add_argument(
    '-d',
    '--database_name',
    type=str,
    default='interactome-test',
    help='name of the database. Defaults to "interactome-test".'
)

if __name__ == '__main__':
    # parse arguments
    args = parser.parse_args()
    # start the interface
    interface = MongoDBInterface(
        uri=args.uri, database_name=args.database_name
    )
    # parse edge list an update the graph
    interface.from_edge_list_filepath(
        args.filepath, Drug, Gene
    )
    # get adjacency
    adjacency, index_mapping_df = interface.get_adjacency(
        entity_query={'entity_type': 'gene'},
        relation_query={'relation_type': 'drug', 'relation_subtype': 'D07961'},
        ignore_relation_subtype=True
    )['drug']['adjacency']
    # look at it
    plt.matshow(adjacency.todense())
    plt.show()
