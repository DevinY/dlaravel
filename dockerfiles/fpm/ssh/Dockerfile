#讓Dlaravel-支援SSH環境Sample。
FROM php:7.3.2-fpm

ARG user

#安裝ssh環境 
ENV OSSH_USER ${user:-dlaravel}
RUN apt-get update&&apt-get install -y openssh-server git pwgen
RUN mkdir /var/run/sshd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
    sed -ri 's/#AuthorizedKeysFile/AuthorizedKeysFile/g' /etc/ssh/sshd_config && \
    sed -ri 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
#Docker官方說明文件
#https://hub.docker.com/_/php/
RUN apt-get update && apt-get install -y \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
                #====安裝mcrypt====
                autoconf \
                libc-dev \
                pkg-config \
		libmcrypt-dev \
                #==================
                libsnmp-dev \
                libsmi2-common \
                libsmi2-dev \
                libperl-dev \
                snmp \
		libpng-dev \
		ca-certificates \
		curl \
		xz-utils \
                sudo \
                cron \
                git \
                wget \
                libmagickwand-dev \
                libldb-dev \
                libldap2-dev \
                libsasl2-dev \
                python \
                vim \
                unzip \
                mysql-client \
                zip \
                libgeoip-dev \
                libpq-dev \
                libzip-dev \
                libbz2-dev \
                libgd2-dev \
                libjpeg-dev \
                libgif-dev \
                libxml2-dev \
                apt-utils \
                supervisor \
                wget \
                && docker-php-ext-install -j$(nproc) pdo_mysql mysqli pgsql pdo_pgsql snmp\
                && docker-php-ext-install -j$(nproc) exif hash gettext sockets ctype xml zip pcntl bcmath\
                && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/  \
                && docker-php-ext-install -j$(nproc) gd

#docker-php-ext-install 可安裝外掛大概如下:
#bcmath bz2 calendar ctype curl dba dom enchant exif fileinfo filter ftp gd gettext gmp hash iconv imap interbase intl json ldap mbstring mysqli oci8 odbc opcache pcntl pdo pdo_dblib pdo_firebird pdo_mysql pdo_oci pdo_odbc pdo_pgsql pdo_sqlite pgsql phar posix pspell readline recode reflection session shmop simplexml snmp soap sockets sodium spl standard sysvmsg sysvsem sysvshm tidy tokenizer wddx xml xmlreader xmlrpc xmlwriter xsl zend_test zip

#RUN  pecl install xdebug \
#     pecl install redis \
#     pecl install imagick \
#     && docker-php-ext-enable xdebug

RUN  pecl install redis \
     pecl install imagick 

#建立Dlaravel的使用者
RUN adduser --quiet --disabled-password --shell /bin/bash --home /home/${OSSH_USER} --gecos "User" ${OSSH_USER};echo "${OSSH_USER}:`pwgen`" |chpasswd &&\
echo "dlaravel ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/dlaravel && \
chmod 0440 /etc/sudoers.d/dlaravel

#建立Dlaravel的ssh環境
USER ${OSSH_USER}
RUN mkdir -p /home/${OSSH_USER}/.ssh&&chmod 700 /home/${OSSH_USER}/.ssh
RUN echo "${KEY}" > /home/${OSSH_USER}/.ssh/authorized_keys
RUN chmod 600 /home/${OSSH_USER}/.ssh/authorized_keys

USER root

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

EXPOSE 9000 22
CMD ["sh","-c","/usr/sbin/sshd -D&php-fpm"]
