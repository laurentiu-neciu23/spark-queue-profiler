#!/bin/bash

docker build -t cluster/hadoop ./hadoop
docker-compose build 
docker-compose up 