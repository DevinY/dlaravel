#!/bin/bash
#在Project的目錄下執行composer
command="cd ${PWD##*/};composer"
while test $# -gt 0
do
command="${command} ${1}"
    shift
done
docker-compose exec -u dlaravel php bash -c "${command}"
