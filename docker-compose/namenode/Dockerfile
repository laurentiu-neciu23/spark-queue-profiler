FROM cluster/hadoop:latest

LABEL Author="Neciu Laurentiu Florin"
LABEL Email="laurentiuflorinneciu@gmail.com"

RUN mkdir -p /hadoop/dfs/name

# is this needed
VOLUME /hadoop/dfs/name

COPY ./start.sh /bin/start.sh
RUN chmod a+x /bin/start.sh

CMD ["/bin/start.sh"]