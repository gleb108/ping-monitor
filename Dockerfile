FROM ubuntu:xenial
MAINTAINER Gleb Galkin

ADD crontab /etc/cron.d/pinger-cron

RUN apt-get update && \
    apt-get -y install python cron iputils-ping && \
    mkdir ping-monitor && \
    /usr/bin/crontab /etc/cron.d/pinger-cron && \
    chmod 0644 /etc/cron.d/pinger-cron && \
    touch ./ping-monitor/pinger.log

ADD config.ini /ping-monitor/config.ini
ADD pinger.py /ping-monitor/pinger.py

CMD cron && tail -f /ping-monitor/pinger.log
