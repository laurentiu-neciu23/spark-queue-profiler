#!/bin/bash

echo $1

hdfs dfs -mkdir -p /user/root
hdfs dfs -put ./shakespeare

spark-submit --class SparkWordCount \
             --master yarn \
             --queue $1 \
	     --deploy-mode client \
	     --executor-memory 1g \
	     --name wordcount \
	     --conf "spark.app.id=wordcount" ./spark-laur_2.11-0.28.0.jar hdfs://namenode:9000/user/root/shakespeare 2
