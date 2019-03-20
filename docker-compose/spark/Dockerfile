FROM cluster/hadoop:latest

LABEL Author="Neciu Laurentiu Florin"
LABEL Email="laurentiuflorinneciu@gmail.com"

ENV SPARK_VERSION 2.4.0
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-without-hadoop
ENV SPARK_HOME /usr/spark-${SPARK_VERSION}
ENV SPARK_DIST_CLASSPATH="$HADOOP_PREFIX/etc/hadoop/*:$HADOOP_PREFIX/share/hadoop/common/lib/*:$HADOOP_PREFIX/share/hadoop/common/*:$HADOOP_PREFIX/share/hadoop/hdfs/*:$HADOOP_PREFIX/share/hadoop/hdfs/lib/*:$HADOOP_PREFIX/share/hadoop/hdfs/*:$HADOOP_PREFIX/share/hadoop/yarn/lib/*:$HADOOP_PREFIX/share/hadoop/yarn/*:$HADOOP_PREFIX/share/hadoop/mapreduce/lib/*:$HADOOP_PREFIX/share/hadoop/mapreduce/*:$HADOOP_PREFIX/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin

RUN mkdir -p /spark-benchmarks

# https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-without-hadoop.tgz

RUN curl -sL \
  "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /usr/ \
 && mv /usr/$SPARK_PACKAGE $SPARK_HOME \
&& chown -R root:root $SPARK_HOME

# Install benchmarking tool.
# https://github.com/CODAIT/spark-bench/releases/download/v99/spark-bench_2.3.0_0.4.0-RELEASE_99.tgz
ENV SPARK_BENCH_HOME /usr/spark-bench 

# This is stupid move this to something else
ENV SPARK_BENCH_PACKAGE spark-bench_2.3.0_0.4.0-RELEASE_99.tgz
ENV SPARK_BENCH_PACKAGE_NAME spark-bench_2.3.0_0.4.0-RELEASE
ENV PATH $PATH:${SPARK_BENCH_HOME}/${SPARK_BENCH_PACKAGE_NAME}/bin
RUN mkdir -p $SPARK_BENCH_HOME


RUN curl -sL \
  "https://github.com/CODAIT/spark-bench/releases/download/v99/${SPARK_BENCH_PACKAGE}" \
  | gunzip \
  | tar x -C /usr/ \
 && mv /usr/$SPARK_BENCH_PACKAGE_NAME $SPARK_BENCH_HOME \
&& chown -R root:root $SPARK_BENCH_HOME

ENV SPARK_JARS /usr/spark-bench/spark-bench_2.3.0_0.4.0-RELEASE/lib
COPY ./jars/spark-bench-2.3.0_0.4.0-RELEASE.jar ${SPARK_JARS}
COPY ./jars/spark-bench-launch-2.3.0_0.4.0-RELEASE.jar ${SPARK_JARS}

#start spark ssh server
RUN /etc/init.d/ssh start

CMD ["tail", "-f", "/dev/null"]