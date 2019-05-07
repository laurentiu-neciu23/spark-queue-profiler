FROM cluster/hadoop:latest

LABEL Author="Neciu Laurentiu Florin"
LABEL Email="laurentiuflorinneciu@gmail.com"

RUN apt-get install -y wget
RUN wget https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz
RUN tar xvfz node_exporter-*.*-amd64.tar.gz

EXPOSE 9100

COPY ./start.sh /bin/start.sh
RUN chmod a+x /bin/start.sh
CMD ["/bin/start.sh"]