#!/bin/bash

docker exec -it spark-master start-master.sh
docker exec -it spark-worker1 start-slave.sh spark://spark-master:7077
docker exec -it spark-worker2 start-slave.sh spark://spark-master:7077