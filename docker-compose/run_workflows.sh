#!/bin/bash

shared_folder="spark-shared"

generation_workflows="workflows/kmeans-execute.conf"
perf_workflows="workflows/kmeans-generate.conf"

function split {
  local dir_num=$(echo $1 | tr '/' ' ' | wc -w)
  local directory_path=$(echo $1 | cut -d '/' -f 1-$[$dir_num-1])
  local file_path=$(echo $1 | cut -d '/' -f $dir_num)
  echo  $directory_path
}

function create_workflow {
  local directory_path=$(split $1)
  mkdir -p "./$shared_folder/$directory_path"
  cp "./$1" "./$shared_folder/$directory_path"
}

function remove_workflow {
  local directory_path$(split $1)
  rm "./$shared_folder/$directory_path/$1"
}

create_workflow $generation_workflows
create_workflow $perf_workflows

docker exec -t spark spark-bench.sh "/$shared_folder/$generation_workflows"
docker exec -t spark spark-bench.sh "/$shared_folder/$perf_workflows"

remove_workflow $generation_workflows
remove_workflow $perf_workflows
