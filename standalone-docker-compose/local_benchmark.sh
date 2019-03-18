#!/bin/bash

# docker cp foo.txt mycontainer:/foo.txt
# docker cp mycontainer:/foo.txt foo.txt



function benchmark {
    generate="kmeans-generate.$1.conf"
    execute="kmeans-execute.$1.conf"

    # Copy benchmarks to docker
    docker cp ./workflows spark-master:/spark-benchmarks

    # remove files from hdfs from local 
    docker exec -i spark-master hdfs dfs -rm -r /spark-shared/
    docker exec -i spark-master rm -rf /spark-shared

    # Execute workflows in spark 
    docker exec -t spark-master spark-bench.sh /spark-benchmarks/workflows/$generate
    docker exec -t spark-master spark-bench.sh /spark-benchmarks/workflows/$execute

    # Copy benchmarking results from hdfs to local node to host
    docker exec -i spark-master hdfs dfs -get /spark-shared/ /
    docker cp spark-master:/spark-shared ./results

    # copy results outside folder 
    cp -r ./results ../results.$1

    # discard results
    rm -rf ./results
}

benchmark 'standalone'
