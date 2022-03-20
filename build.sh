#!/bin/bash
#會直接建立image及docker-compose-normal的設定
PREFIX=dlaravel
BASE_ON=docker-compose-normal.yml
read -p "Are you sure want to build tree images dlaravel_web、dlaravel_php and dlaravel_db that base on docker-compose-normal.yaml?(y/n)"

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
yaml() {
    python3 -c "import yaml;print(yaml.safe_load(open('${BASE_ON}'))${KEY})"
}

create_dockerfile(){
    echo "FROM $IMAGE" > Dockerfile_${SERVICE}
    KEY="['services']['${SERVICE}']['volumes']"
    VOLUMES=$(yaml $KEY)
    for volume in ${VOLUMES}; 
    do
        if [ ${SERVICE} == "php" ]; then
            echo $volume|grep -qE 'etc/cache:|sites:|data:'
            if [ $? -eq 1 ]; then
                echo "COPY ${volume}"|sed 's/:/\/\. /g'|sed -E "s/\[|\]|[\']|[\"]|,$//g" >> Dockerfile_${SERVICE}
            fi
            echo EXPOSE 9000 >> Dockerfile_${SERVICE}
            echo USER dlaravel >> Dockerfile_${SERVICE}
            echo CMD [\"php-fpm\"] >> Dockerfile_${SERVICE}
        fi

        if [ ${SERVICE} == "web" ]; then
            echo $volume|grep -qE 'sites:'
            if [ $? -eq 1 ]; then
                echo "COPY ${volume}"|sed 's/:/\/*.conf /g'|sed -E "s/\[|\]|[\']|[\"]|,$//g" >> Dockerfile_${SERVICE}
                echo "COPY ./etc/ssl /etc/nginx/conf.d/ssl" >> Dockerfile_${SERVICE}
            fi
        fi

        if [ ${SERVICE} == "db" ]; then
            echo $volume|grep -qE 'data:'
            if [ $? -eq 1 ]; then
                echo "COPY ${volume}"|sed 's/:/\/\. /g'|sed -E "s/\[|\]|[\']|[\"]|,$//g" >> Dockerfile_${SERVICE}
            fi
        fi
    done
}

SERVICE=php
KEY="['services']['${SERVICE}']['image']"
IMAGE=$(yaml $KEY)
create_dockerfile
docker build -t ${PREFIX}_${SERVICE} -f Dockerfile_${SERVICE} .

SERVICE=web
KEY="['services']['${SERVICE}']['image']"
IMAGE=$(yaml $KEY)
create_dockerfile
docker build -t ${PREFIX}_${SERVICE} -f Dockerfile_${SERVICE} .

SERVICE=db
KEY="['services']['${SERVICE}']['image']"
IMAGE=$(yaml $KEY)
create_dockerfile
docker build -t ${PREFIX}_${SERVICE} -f Dockerfile_${SERVICE} .
fi
