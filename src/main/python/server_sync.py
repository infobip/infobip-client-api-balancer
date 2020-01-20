import requests

from backup import backup_servers
from haproxy_config_reader import BackendConfigurationService


def sync(logger, url, authorization, connectTimeout, readTimeout):
    servers = requests.get(url=url, headers={"Authorization": authorization}, timeout=(connectTimeout, readTimeout)).json()
    set_servers(logger, servers)
    backup_servers(logger, servers)
    return True


def set_servers(logger, servers):
    logger.info("Servers: " + str(servers))
    backend_configuration_service = BackendConfigurationService(host="127.0.0.1", port=9999)
    i = 0
    skip = 0
    for backend_server in backend_configuration_service.find_servers("api_backend"):
        if not backend_server.be_name == "api_backend":
            continue
        if not backend_server.srv_name.startswith("api_srv"):
            continue
        if skip > 0:
            skip = skip - 1
            continue
        if len(servers) > i:
            server = servers[i]
            skip = backend_configuration_service.set_real_server(backend_server.be_name, int(backend_server.srv_id),
                                                                 server["hostname"], 443) - 1

            logger.info("ENABLED: " + str(backend_server))
        else:
            skip = backend_configuration_service.set_fake_server(backend_server.be_name, int(backend_server.srv_id)) - 1
            logger.info("DISABLED: " + str(backend_server))
        i = i + 1
