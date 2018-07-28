#!/bin/bash
if [ -d "sites/" ]; then
    echo "Add alias as below, than you can run phpunit in your project folder."
    echo 'alias phpunit="../../phpunit.sh"'
    exit;
fi
docker-compose -f "../../docker-compose.yml" exec -u dlaravel php $(basename `pwd`)/vendor/bin/phpunit -c $(basename `pwd`)/phpunit.xml
