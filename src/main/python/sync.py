#!/usr/bin/env python3

import logging
import os
import time
from logging.handlers import RotatingFileHandler

import server_sync
from backup import load_servers_from_backup
from util import ensure_dir

SYNC_DISABLED = os.environ.get("SYNC_DISABLED", 'False')
SYNC_SCHEDULED = os.environ.get("SYNC_SCHEDULED", 'True')
SECONDS_BETWEEN_SYNCS = os.environ.get("SECONDS_BETWEEN_SYNCS", '60')
LOG_DIR = ensure_dir(os.environ.get("LOG_DIR", "/var/log/haproxy-sync"))
ENDPOINTS_URL = os.environ.get("ENDPOINTS_URL", "https://api.infobip.com/client/v1/balancer/endpoints")
ENDPOINTS_AUTHORIZATION = os.environ.get("ENDPOINTS_AUTHORIZATION", "App UNAUTHORIZED")
ENDPOINTS_CONNECT_TIMEOUT = float(os.environ.get("ENDPOINTS_CONNECT_TIMEOUT", "2"))
ENDPOINTS_READ_TIMEOUT = float(os.environ.get("ENDPOINTS_READ_TIMEOUT", "10"))

logger = logging.getLogger("sync")
logger.setLevel(logging.DEBUG)
fh = RotatingFileHandler("{}/sync.log".format(LOG_DIR), maxBytes=10 * 1024 * 1024, backupCount=10, delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

scheduled = "true" == SYNC_SCHEDULED.lower()
disabled = "true" == SYNC_DISABLED.lower()
pause = int(SECONDS_BETWEEN_SYNCS)

load_servers_from_backup(logger)

while True:
    if not disabled:
        try:
            logger.info("Executing backend servers sync ...")
            if server_sync.sync(logger, ENDPOINTS_URL, ENDPOINTS_AUTHORIZATION, ENDPOINTS_CONNECT_TIMEOUT, ENDPOINTS_READ_TIMEOUT):
                logger.info("Backend servers sync success")
            else:
                logger.info("Backend servers sync error")
        except Exception as e:
            logger.exception('Backend servers sync error', exc_info=e)
    if scheduled:
        time.sleep(pause)
    else:
        break
