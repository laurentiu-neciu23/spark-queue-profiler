#!/bin/bash
echo $HADOOP_PREFIX
echo $HADOOP_CONF_DIR

# Start namenode
$HADOOP_PREFIX/bin/hdfs --config $HADOOP_CONF_DIR datanode
