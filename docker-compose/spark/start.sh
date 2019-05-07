#!/bin/bash

# Start node exporter
cd node_exporter-*.*-amd64 && ./node_exporter > node_exporter.log &

tail -f /dev/null