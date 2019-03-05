FROM cluster/hadoop:latest

LABEL Author="Neciu Laurentiu Florin"
LABEL Email="laurentiuflorinneciu@gmail.com"

# tcp        0      0 0.0.0.0:44065           0.0.0.0:*               LISTEN      6/java              
# tcp        0      0 0.0.0.0:8040            0.0.0.0:*               LISTEN      6/java              
# tcp        0      0 0.0.0.0:8042            0.0.0.0:*               LISTEN      6/java   

COPY ./start.sh /bin/start.sh
RUN chmod a+x /bin/start.sh
CMD ["/bin/start.sh"]