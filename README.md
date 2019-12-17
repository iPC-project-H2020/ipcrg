# iPC relational graph

<p align="center">
  <img src="./docs/_static/logo.png" alt="ipc-logo" width=500>
</p>

Package to ingest/generate and query relational graphs. For the full documentation see the dedicated [website](https://ipc-project-h2020.github.io/ipcrg/).

## `ipcrg` executables

Ingesting entities from the id mapping resources:

```console
$ ipcrg-entities-from-resources -h
usage: ipcrg-entities-from-resources [-h] [-u URI] [-i {mongo}] -d
                                     DATABASE_NAME

optional arguments:
  -h, --help            show this help message and exit
  -u URI, --uri URI     uri connection string. Defaults to
                        "mongodb://localhost:27017/".
  -i {mongo}, --interface {mongo}
                        interface type. Defaults to "mongo".
  -d DATABASE_NAME, --database_name DATABASE_NAME
                        name of the database.
```

Ingesting relations from an edge list in .csv or .gr format:

```console
$ ipcrg-parse-edge-list -h
usage: ipcrg-parse-edge-list [-h] -f FILEPATH [-u URI] [-i {mongo}] -d
                             DATABASE_NAME --source_entity
                             {gene,protein,patient}
                             [--target_entity {gene,protein,patient}]
                             --relation
                             {curie,drug,mondo,ppi,biogrid,reactome,recon3d-metabolite}
                             [--source_entity_parameters SOURCE_ENTITY_PARAMETERS]
                             [--target_entity_parameters TARGET_ENTITY_PARAMETERS]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        path to the edge list in .csv or .gr format.
  -u URI, --uri URI     uri connection string. Defaults to
                        "mongodb://localhost:27017/".
  -i {mongo}, --interface {mongo}
                        interface type. Defaults to "mongo".
  -d DATABASE_NAME, --database_name DATABASE_NAME
                        name of the database.
  --source_entity {gene,protein,patient}
                        type of source entities.
  --target_entity {gene,protein,patient}
                        type of target entities. If not provided defaults to
                        source_entity.
  --relation {curie,drug,mondo,ppi,biogrid,reactome,recon3d-metabolite}
                        type of relation.
  --source_entity_parameters SOURCE_ENTITY_PARAMETERS
                        optional parameters to build source entities in JSON
                        format.
  --target_entity_parameters TARGET_ENTITY_PARAMETERS
                        optional parameters to build source entities in JSON
                        format. If not provided defaults to
                        source_entity_parameters.
```

Create indexes via the database interface:

```console
$ ipcrg-create-indexes -h
usage: ipcrg-create-indexes [-h] [-u URI] [-i {mongo}] -d DATABASE_NAME

optional arguments:
  -h, --help            show this help message and exit
  -u URI, --uri URI     uri connection string. Defaults to
                        "mongodb://localhost:27017/".
  -i {mongo}, --interface {mongo}
                        interface type. Defaults to "mongo".
  -d DATABASE_NAME, --database_name DATABASE_NAME
                        name of the database.
```

## development setup

### setup a `venv`

Create and activate a `venv`:

```sh
python3 -m venv venv
source venv/bin/activate
```

### install dependencies

Install package dependencies:

```sh
pip install -r requirements.txt
```

Install packages used for styling and development:

```sh
pip install -r dev_requirements.txt
```

Install the package in editable mode:

```sh
pip install -e .
```

### run database using `docker-compose`

To spawn the database just run:

```sh
docker-compose -f docker/docker-compose.yml up -d
```

To tear it down run:

```sh
docker-compose -f docker/docker-compose.yml down
```

**NOTE:** the data in the container are not persisted on a physical volume. In order to store data, a volume should be configured an mounted.

## examples

After spawning the database:

```sh
docker-compose -f docker/docker-compose.yml up -d
```

Parse ppi from a CSV file:

```sh
python examples/ppi_example.py -f data/interactions.csv
```

Parse drug-based interaction from a GR file (space-separated values):

```sh
python examples/play_ground.py -f data/KEGG_drugs.19-10-2019.gr
```
