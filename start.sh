#!/bin/bash
#引数には、$command "URL"

$conffile="/etc/nginx/nginx.conf"
for i in `seq 1 100`
do
    #confの値を変更
    python readconf.py $conffile $i
    #nginxのリロード
    sudo ngiinx -t
    sudo nginx -s reload 
    #実験
    locust -f locustfile.py \
    --headless -u 10000 -r 1000 \
    --run-time 3m \
    --csv=example$i \
    --host $1 & top -b -n 180 -d 1 | grep nginx >> log$i.txt


done