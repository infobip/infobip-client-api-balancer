import json
from os import path

from util import ensure_dir


def backup_servers(logger, servers):
    servers_file = ensure_dir("/tmp/infobip-client-api-balancer") + "/servers.json"
    try:
        with open(servers_file, "w") as data_file:
            json.dump(servers, data_file, indent=4, sort_keys=True)
    except Exception as e:
        logger.exception('Error saving backup', exc_info=e)


def load_servers_from_backup(logger):
    from server_sync import set_servers

    servers_file = ensure_dir("/tmp/infobip-client-api-balancer") + "/servers.json"
    if not path.exists(servers_file):
        return
    try:
        with open(servers_file, "r+") as data_file:
            servers = json.load(data_file)
        set_servers(logger, servers)
    except Exception as e:
        logger.exception('Error loading backup', exc_info=e)
