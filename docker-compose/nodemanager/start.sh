#!/bin/bash

# Start node exporter
cd node_exporter-*.*-amd64 && ./node_exporter > node_exporter.log &


$HADOOP_PREFIX/bin/yarn --config $HADOOP_CONF_DIR nodemanager
