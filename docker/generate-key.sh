#!/usr/bin/env bash
set -e

openssl req -subj "/CN=*.localhost.com/O=Localhost Ltd/C=HR" -new -newkey rsa:2048 -days 3650 -nodes -x509 -keyout server.key -out server.crt
cat server.key server.crt | tee haproxy.pem
rm server.key server.crt
