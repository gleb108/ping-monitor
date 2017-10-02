#!/usr/bin/env python

from ConfigParser import SafeConfigParser
import subprocess
import logging
import pickle

def alert (ip, status):
    txt = "{0} ({1}) - {2}".format(host[ip], ip, status)
    cmd = '{0} https://api.telegram.org/bot{1}/sendMessage -d "chat_id={2}&text={3}"'.format(
          telegram_send_command, telegram_bot_id, telegram_chat_id, txt)
    print cmd
    logger.info('Send notification: %s (%s) - %s', host[ip], ip, status)
#    subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
 


parser = SafeConfigParser()
parser.read("config.ini")
log = parser.get("main", "log")
filestatus = parser.get("main", "status")

check_command = parser.get("check", "host_check")
connectivity_check_command = parser.get("check", "connectivity_check")

telegram_chat_id = parser.get("telegram", "chat_id")
telegram_bot_id = parser.get("telegram", "bot_id")
telegram_send_command = parser.get("telegram", "send_command")

logger = logging.getLogger('pinger')
hdlr = logging.FileHandler(log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


host={}
host_status={}
hosts = parser.items("hosts")
for line in hosts:
    ip = line[0]
    name = line[1]
    host[ip] = name

#connectivity_check
logger.debug(connectivity_check_command)
retcode = subprocess.call(connectivity_check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
if (retcode):
   logger.info('No connectivity. Exit')
   exit(1)
else: 
   logger.debug("Connectivity check passed")

#checking hosts
for ip in host.keys():
    cmd = check_command + ' ' + ip
    retcode = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    host_status[ip]=retcode
    if (retcode):
        logger.debug("%s %s - DOWN", host[ip], ip)
    else:
        logger.debug("%s %s - UP", host[ip], ip)

try:
    with open(filestatus, "rb") as StatusFile:
        last_status = pickle.load(StatusFile)
except IOError:
    StatusFile = open(filestatus,'w')
    pickle.dump(host_status, StatusFile)
    logger.info('Save current status to the file %s', filestatus)
    logger.info('Exit')
    exit(1)
    


for ip in host_status.keys():
    try:
        print ip, host_status[ip], last_status[ip]
        if (host_status[ip] != last_status[ip]):
           if (host_status[ip]):
              status = 'DOWN'
           else: 
              status = 'UP'

           alert(ip,status) 
    except KeyError: 
        logger.info('Last status for %s not found, ignoring', host[ip])

with open(filestatus, "wb") as StatusFile:  
    pickle.dump(host_status, StatusFile)
    logger.info('Save current status to the file %s', filestatus)

