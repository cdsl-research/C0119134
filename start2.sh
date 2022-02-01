   
#!/bin/bash
#引数には、$command "URL"

conffile="/etc/nginx/nginx.conf"
mkdir kkc1 kkl1 kkl2 kkc2
for i in `seq 5 5 100`
do
    echo $i
    #confの値を変更
    sudo python3 readconf.py $conffile $i
    #nginxのリロード
    sudo nginx -t
    sudo nginx -s reload 
    #実験
    locust -f locustfile1.py \
    --headless -u 500 -r 50 \
    --run-time 3m \
    --csv=kkc1/example$i \
    --host $1 & top -b -n 180 -d 1 | grep nginx >> kkl1/log$i.txt
done
python3 paretoptint1.py
for k in `cat paretofront.txt`
do
    sudo python3 readconf.py $conffile $k
    #nginxのリロード
    sudo nginx -t
    sudo nginx -s reload
    #実験
    locust -f locustfile1.py \
    --headless -u 500 -r 50 \
    --run-time 3m \
    --csv=kkc2/example$k \
    --host $1 & top -b -n 180 -d 1 | grep nginx >> kkl2/log$k.txt
done
python3 paretoptint1.py
op=$(tail paretofront.txt -n -1)
sudo readconf.py $conffile $op
