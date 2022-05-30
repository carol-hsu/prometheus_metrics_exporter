#!/bin/bash

PROM_URL=http://10.103.174.69:9090

CNAME="my-registry"
FUNC=rate
RANGE=1m
FREQ=15
FROM=20
PERIOD=10

python prom_query.py $PROM_URL 'container_cpu_usage_seconds_total{namespace="default",container="'$CNAME'"}' $FUNC $RANGE $FREQ $FROM $PERIOD
