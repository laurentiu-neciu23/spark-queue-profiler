#!/bin/bash

# docker cp foo.txt mycontainer:/foo.txt
# docker cp mycontainer:/foo.txt foo.txt


function benchmark {
    generate="kmeans-generate.$1.conf"
    execute="kmeans-execute.$1.conf"

    # Copy benchmarks to docker
    docker cp ./workflows spark:/spark-benchmarks

    # remove files from hdfs from local 
    docker exec -i spark hdfs dfs -rm -r /spark-shared/
    docker exec -i spark rm -rf /spark-shared

    # Execute workflows in spark 
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$generate
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$execute

    # Copy benchmarking results from hdfs to local node to host
    docker exec -i spark hdfs dfs -get /spark-shared/ /
    docker cp spark:/spark-shared ./results

    # copy results outside folder 
    cp -r ./results ../results.$1

    # discard results
    rm -rf ./results
}

function singleton_benchmark {

    rm -rf "./tmp"

    # Generators and executors (generators are the same)
    generate="singleton-kmeans-generate.$1.conf"
    execute="singleton-kmeans-execute.$1.conf"
    regex="^|.*"

    mkdir -p "./tmp/"
    docker cp ./workflows spark:/spark-benchmarks

    echo "=========== GENERATION ==========="
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$generate

    echo "=========== EXECUTION AND REDIRECT ==========="
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$execute > "./tmp/temporary_console_data"
    cat "./tmp/temporary_console_data" | grep $regex | tr -d " " | tr "|" "," | cut -d, -f2- > "./tmp/unsanitized_dataset"
    
    rm -rf ./res
    python split.py
    mv ./res ../results.$1

    rm -rf "./tmp"

}


function generate_hdfs_data {
    generate="kmeans-generate.yarn.conf"
    docker cp ./workflows spark:/spark-benchmarks

    # Generate 
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$generate
}

# Function to load sql
# Function to load kmeans
# Function to load pi
function load {
    execute="load.$1.conf"
    docker exec -t spark spark-bench.sh /spark-benchmarks/workflows/$execute

    docker exec -i spark hdfs dfs -get /spark-shared/ /
    docker cp spark:/spark-shared ./results

    # copy results outside folder 
    cp -r ./results ../results.$1

    # discard results
    rm -rf ./results
}

if [ "$1" == "--function"  ]
then
    if [ "$2" == "generate" ]
    then
        generate_hdfs_data
    fi

    if [ "$2" == "sql" ]
    then
        load "sql"
    fi

    if [ "$2" == "kmeans" ]
    then
        load "kmeans"
    fi

    if [ "$2" == "pi" ]
    then
        load "pi"
    fi
fi
