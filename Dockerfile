FROM haproxy:2.1.0-alpine

EXPOSE 8080
EXPOSE 8443
EXPOSE 8182

ENTRYPOINT []
CMD ["supervisord", "--nodaemon", "--configuration", "/usr/local/etc/supervisord.conf"]

RUN apk --no-cache add socat python3 supervisor bash openssl

COPY src/main/python/ /opt/haproxy-sync/
COPY requirements.txt /opt/haproxy-sync/requirements.txt

COPY docker/ /

RUN pip3 install -r /opt/haproxy-sync/requirements.txt \
    && chmod +x /*.sh \
    && mkdir -p /var/log/supervisor/ \
    && chmod +x /opt/haproxy-sync/sync.py \
    && mkdir -p /var/log/haproxy-sync/ \
    && mkdir -p /usr/local/etc/haproxy/cert/ \
    && cd /usr/local/etc/haproxy/cert/ \
    && /generate-key.sh

ENV INFOBIP_CLIENT_API_BALANCER_VERSION=latest