# iPC deliverables


## D5.1

To reproduce the relational graph supported by ipcrg just run (from the root of the repo):

```sh
sh scripts/deliverables/d5.1-graph-construction.sh
```

*NOTE:* the script accepts an argument pointing to a Mongo DB uri. By default it will connect to `mongodb://localhost:27017/`. In case no database is available the script will fail. To test that everytihng runs smoothly you can spawn a Mongo DB instance by using the [docker-compose.yml](../../docker/docker-compose.yml) provided.

