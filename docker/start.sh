#!/usr/bin/env sh
set -e

exec /usr/local/sbin/haproxy -f /usr/local/etc/haproxy/haproxy.cfg -W -db
