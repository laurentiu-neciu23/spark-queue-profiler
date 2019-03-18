FROM debian:9

LABEL Author="Neciu Laurentiu Florin"
LABEL Email="laurentiuflorinneciu@gmail.com"

# Fetch indexes
RUN apt-get update

# Install java
RUN apt-get install -y --no-install-recommends openjdk-8-jdk
RUN apt-get install -y ssh
# Install python for required apps
RUN apt-get install -y python-pip
RUN pip install yq

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

RUN apt-get install -y --no-install-recommends curl 

# Install hadoop
ENV HADOOP_VERSION 3.1.2
ENV HADOOP_URL https://www.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz

RUN curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && tar -xvf /tmp/hadoop.tar.gz -C /opt/ \
    && rm /tmp/hadoop.tar.gz

RUN ln -s /opt/hadoop-$HADOOP_VERSION/etc/hadoop /etc/hadoop
RUN mkdir /opt/hadoop-$HADOOP_VERSION/logs

# Env
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=/etc/hadoop

ENV USER=root
ENV HADOOP_PREFIX=/opt/hadoop-$HADOOP_VERSION
ENV PATH $HADOOP_PREFIX/bin/:$PATH

# Parsing goodies
RUN apt-get install -y jq
RUN apt-get install -y bc

# Copy configurations 
COPY ./config/core-site.xml /etc/hadoop/core-site.xml
COPY ./config/hdfs-site.xml /etc/hadoop/hdfs-site.xml
COPY ./config/mapred-site.xml /etc/hadoop/mapred-site.xml
COPY ./config/yarn-site.xml /etc/hadoop/yarn-site.xml
# COPY ./config/capacity-scheduler.xml /etc/hadoop/capacity-scheduler.xml



