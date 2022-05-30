#!/bin/bash

PROM_URL=http://10.103.174.69:9090

OUTPUT="./output/obj-detect"
POD_NAME="obj-detect"
CNAME="tf-server"
FUNC=rate
RANGE=1m
FREQ=10
FROM=39
PERIOD=5

echo "========== CPU ==========" > ${OUTPUT}_cpu
python prom_query.py $PROM_URL 'container_cpu_usage_seconds_total{namespace="default",pod=~"'$POD_NAME'.*",container="'$CNAME'"}' $FUNC $RANGE $FREQ $FROM $PERIOD >> ${OUTPUT}_cpu

echo "======== Memory ========" > ${OUTPUT}_mem
python prom_query.py $PROM_URL 'container_memory_working_set_bytes{namespace="default",pod=~"'$POD_NAME'.*",container="'$CNAME'"}' none none $FREQ $FROM $PERIOD >> ${OUTPUT}_mem

echo "====== Recv Bytes ======" > ${OUTPUT}_ig_bytes
python prom_query.py $PROM_URL 'container_network_receive_bytes_total{namespace="default",pod=~"'$POD_NAME'.*"}' $FUNC $RANGE $FREQ $FROM $PERIOD >> ${OUTPUT}_ig_bytes

echo "====== Recv Packets ======" > ${OUTPUT}_ig_pkts
python prom_query.py $PROM_URL 'container_network_receive_packets_total{namespace="default",pod=~"'$POD_NAME'.*"}' $FUNC $RANGE $FREQ $FROM $PERIOD >> ${OUTPUT}_ig_pkts


echo "====== Send Bytes ======" > ${OUTPUT}_eg_bytes
python prom_query.py $PROM_URL 'container_network_transmit_bytes_total{namespace="default",pod=~"'$POD_NAME'.*"}' $FUNC $RANGE $FREQ $FROM $PERIOD >> ${OUTPUT}_eg_bytes

echo "====== Send Packets ======" > ${OUTPUT}_eg_pkts
python prom_query.py $PROM_URL 'container_network_transmit_packets_total{namespace="default",pod=~"'$POD_NAME'.*"}' $FUNC $RANGE $FREQ $FROM $PERIOD >> ${OUTPUT}_eg_pkts



