#!/usr/bin/env bash

docker rm -f infobip-client-api-balancer

mkdir -p $(pwd)/local/run/logs/haproxy-sync/
mkdir -p $(pwd)/local/run/logs/supervisor/
mkdir -p $(pwd)/local/run/tmpinfobip-client-api-balancer/

docker run \
    -v $(pwd)/local/run/logs/haproxy-sync:/var/log/haproxy-sync \
    -v $(pwd)/local/run/logs/supervisor:/var/log/supervisor \
    -v $(pwd)/local/run/tmp/infobip-client-api-balancer/:/tmp/infobip-client-api-balancer/ \
    -v $(pwd)/docker/usr/local/etc/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg \
    -e "ENDPOINTS_AUTHORIZATION=$ENDPOINTS_AUTHORIZATION" \
    -p 7070:7070 \
    -p 7443:7443 \
    -p 7182:7182 \
    -p 9999:9999 \
    --name infobip-client-api-balancer \
    -d infobip-client-api-balancer:latest

docker logs -f infobip-client-api-balancer
