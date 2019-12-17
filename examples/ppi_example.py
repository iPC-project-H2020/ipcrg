"""Building a relational graph for proteins with MongoDB backend."""
import argparse
import matplotlib.pyplot as plt
from ipcrg.interfaces.mongo import MongoDBInterface
from ipcrg.entities.protein import Protein
from ipcrg.relations.ppi import PPI

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
        args.filepath, PPI, Protein
    )
    # get adjacency
    adjacency, index_mapping_df = interface.get_adjacency(
        entity_query={'entity_type': 'protein'},
        relation_query={'relation_type': 'ppi'},
        ignore_relation_subtype=True
    )['ppi']['adjacency']
    # look at it
    plt.matshow(adjacency.todense())
    plt.show()
