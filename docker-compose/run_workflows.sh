#!/bin/bash

shared_folder="spark-shared"

generation_workflows="workflows/kmeans-execute.conf"
perf_workflows="workflows/kmeans-generate.conf"

function create_folders {
  dir_num=$(echo $1 | tr '/' ' ' | wc -w)
  directory_path=$(echo $1 | cut -d '/' -f 1-$[$dir_num-1])
  file_path=$(echo $1 | cut -d '/' -f $dir_num)
  echo $directory_path
  echo $file_path

  mkdir -p "./$shared_folder/$directory_path"
  cp "./$1" "./$shared_folder/$directory_path"
}

create_folders $generation_workflows
create_folders $perf_workflows

# todo if many workflows 
echo "/$shared_folder/$generation_workflows"
docker exec -t spark spark-bench.sh "/$shared_folder/$generation_workflows"
docker exec -t spark spark-bench.sh "/$shared_folder/$perf_workflows"

