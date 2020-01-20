#!/usr/bin/env bash

n=0
until [ $n -ge 100 ]
do
    docker build -t infobip-client-api-balancer:latest .
    [ $? -eq 0 ] && exit 0
    n=$[$n+1]
    sleep 1
done
