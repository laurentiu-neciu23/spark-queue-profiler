#!/bin/bash
echo $HADOOP_PREFIX
echo $HADOOP_CONF_DIR

function fetch_namedir {
  length=$(cat /etc/hadoop/hdfs-site.xml | xq -y .configuration.property | wc -l | xargs -I% echo %/2 | bc)
  for i in $(seq $length); do 
    property=$(cat /etc/hadoop/hdfs-site.xml | xq -y .configuration.property[$(echo $i-1 | bc)]); 

    # fetch namenode from config file
    if [ "`echo $property | grep 'namenode.name.dir'`" != "" ]; then
      namenode_dir=$property
    fi
  done
  echo $namenode_dir | tr -s " " | cut -d " " -f4
}

namedir=$(fetch_namedir)
echo $namedir "============== NAMEDIR"

if [ "`ls -A $namedir`" == "" ]; then
  echo "Formatting namenode name directory: $namedir"
  $HADOOP_PREFIX/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME 
fi

# Start namenode
$HADOOP_PREFIX/bin/hdfs --config $HADOOP_CONF_DIR namenode
