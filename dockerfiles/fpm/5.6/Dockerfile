FROM php:5.6.34-fpm
MAINTAINER Devin Yang <devin@ccc.tc>
#Docker官方說明文件
#https://hub.docker.com/_/php/
RUN apt-get update && apt-get install -y \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
		libmcrypt-dev \
		libpng-dev \
		ca-certificates \
		curl \
		xz-utils \
                sudo \
                cron \
                git \
                wget \
                libldap2-dev \
                libsasl2-dev \
                python \
                vim \
                unzip \
                mysql-client \
                zip \
                libpq-dev \
                libzip-dev \
                libbz2-dev \
                libgd2-dev \
                libpng12-0 \
                libpng12-dev \
                libjpeg-dev \
                libgif-dev \
                libxml2-dev \
                apt-utils \
                supervisor \
                wget \
	&& docker-php-ext-install -j$(nproc) mcrypt pdo_mysql mysqli pgsql pdo_pgsql ftp \
        dba exif sockets xml tokenizer zip bz2 gettext pcntl dom \
	&& docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-jpeg-dir --with-png-dir --with-gif-dir \
        --enable-opacache-file --enable-exif --enable-sqlite-utf8 --enable-zip --enable-pcntl \
        --with-fpm-user=dlaravel --with-fpm-group=dlaravel \
        --with-curl --with-libedit --with-openssl --with-zlib \
        --with-phpdbg-debug --with-debug \
        --with-ldap --with-ldap-sasl \
	&& docker-php-ext-install -j$(nproc) gd

RUN pecl install xdebug-2.5.5 \
	&& docker-php-ext-enable xdebug

#建立Dlaravel的使用者
RUN adduser --disabled-password --gecos "" dlaravel &&\
echo "dlaravel ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/dlaravel && \
chmod 0440 /etc/sudoers.d/dlaravel

#安裝composer
RUN EXPECTED_SIGNATURE=$(wget -q -O - https://composer.github.io/installer.sig); \
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"; \
ACTUAL_SIGNATURE=$(php -r "echo hash_file('SHA384', 'composer-setup.php');"); \
php composer-setup.php; \
php -r "unlink('composer-setup.php');"; \
mv composer.phar /usr/local/bin/composer; \ 
#加入dlaravel使用者
sudo -u dlaravel /usr/local/bin/composer global require "laravel/installer"; \
sudo -u dlaravel /usr/local/bin/composer global require "phpunit/phpunit=5.5.*"; \
sudo -u dlaravel echo 'export TERM=xterm-256color' >> /home/dlaravel/.bashrc; \
sudo -u dlaravel echo 'export PATH=/home/dlaravel/.composer/vendor/bin:$PATH' >> /home/dlaravel/.bashrc; \
#加入composer環境變數
echo 'export TERM=xterm-256color' >> /root/.bashrc; \
echo 'export PATH=/root/.composer/vendor/bin:$PATH' >> /root/.bashrc;  

EXPOSE 9000
CMD ["php-fpm"]
