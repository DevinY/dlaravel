#!/bin/bash
if [ -d "sites/" ]; then
    echo "Add alias as below, than you can run php artisan in your project folder."
    echo 'alias a="../../artisan.sh"'
    exit;
fi
docker-compose -f "../../docker-compose.yml" exec -u dlaravel php php $(basename `pwd`)/artisan ${@}
