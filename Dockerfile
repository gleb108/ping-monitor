FROM ubuntu:xenial
MAINTAINER Gleb Galkin

ADD crontab /etc/cron.d/pinger-cron

RUN apt-get update && \
    apt-get -y install git python cron iputils-ping && \
    git clone https://github.com/gleb108/ping-monitor

RUN /usr/bin/crontab /etc/cron.d/pinger-cron
RUN chmod 0644 /etc/cron.d/pinger-cron

ADD config.ini /ping-monitor/config.ini
RUN touch ./ping-monitor/pinger.log

CMD cron && tail -f /ping-monitor/pinger.log
