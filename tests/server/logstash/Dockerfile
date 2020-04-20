FROM logstash:7.6.0

RUN bin/logstash-plugin install logstash-output-mongodb
#COPY logstash.conf ./pipeline

ENTRYPOINT ["logstash", "--config.reload.automatic"]
