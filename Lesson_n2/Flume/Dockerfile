FROM probablyfine/flume:latest

ADD flume.conf /var/tmp/flume.conf

EXPOSE 44444

ENTRYPOINT [ "flume-ng", "agent", "-c", "/opt/flume/conf", "-f", "/var/tmp/flume.conf", "-n", "docker", "-Dflume.root.logger=INFO,console" ]