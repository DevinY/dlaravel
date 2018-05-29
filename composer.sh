#!/bin/bash
#在Project的目錄下執行composer
docker-compose exec -u dlaravel php bash -c "cd ${PWD##*/};composer $1"
