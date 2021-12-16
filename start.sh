#!/bin/bash
$name=`hostname -I`
#lakdjf
locust -f locustfile.py \
--headless -u 10000 -r 1000 \
--run-time 3m \
--csv=example \
--host http://$name/ & top | grep nginx >> log.txt