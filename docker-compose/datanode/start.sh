#!/bin/bash
echo $HADOOP_PREFIX
echo $HADOOP_CONF_DIR

# Start node exporter
cd node_exporter-*.*-amd64 && ./node_exporter > node_exporter.log &

# Start namenode
$HADOOP_PREFIX/bin/hdfs --config $HADOOP_CONF_DIR datanode
