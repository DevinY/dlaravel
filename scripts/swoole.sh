#!/usr/bin/env bash

dir=/var/www/html/${1}

php /var/www/html/${1}/bin/laravels -d start

inotifywait -rm "$dir" --format '%w%f' -e modify |
    while read file; do
	if [[ $file == *.php ]]; then
	   php /var/www/html/${1}/bin/laravels reload
	   echo $file
	fi
    done

/usr/local/sbin/php-fpm
