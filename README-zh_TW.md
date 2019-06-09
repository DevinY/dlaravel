
**[English Documentation](https://github.com/DevinY/dlaravel/blob/master/README.md)**

# D-Laravel (開發&學習)

想要有 Docker + Laravel 建立PHP開發環境嗎，D-Laravel使用了docker-compose，

他讓我們可透過自訂docker-compose-custom.yml輕易的擴充更多的服務，打造自己的微服務架構。

經由超簡易的console及create指令，讓您更簡單的建立出Laravel或PHP開發或學習環境。

D-Laravel，代表了，我們的Mac系統，不再需要安裝mysql、nginx、php-fpm或者NodeJs。


### 為什麼用D-Laravel

提供簡易方式執行docker-compose指令，快速生成laravel專案環境，而且還自動替您建立資料庫及調整Laravel的.env資料庫設定。

可安裝sublime3外掛D-Laravel alias，經由sublime執行容器內的artisan及composer命令(MacOS及Linux環境)。

可用最新的PHP在Mac OS、Linux、Widnows 10的gitbash環境執行。

快速產生self-signed自我簽署的憑證，並完成HTTPS設定。

不需要安裝DnsMasq軟體。

D-laravel停止時，不會佔用80埠，拜docker-compose之賜，極易調整Listen的連接埠。

秒級的啟動速度。

可模擬不同的資料庫環境。

可同時開啟多個不同的測試站台。

使用Dockerhub標註offical的image，建立Laravel基本執行環境。

用docker聽起來，好像比較潮。:p
<pre>
./console help (幫助，console參數用法。)
./create test1  (建立test1.test)
./console down或./console up (啟用及停用container)
./console restart    (./console down再./console up)
`./console alias`  
(打./console指令太長了嗎，上方指令可暫時用c代表./console，所以執行後，輸入:c info、c up或c down..即可執行。)
./console alias    (印出console的別名範本，自行加到.bashrc或.zshrc永久生效)
./console version  (顯示D-Laravel的版本)

產生自我簽署憑證給目前所有的Project. (MacOS or Linux)。
./console secure
</pre>

#### D-Laravel易懂目錄結構
<pre>
etc/   (nginx、php.ini及mysql的相關設定檔)
data/  (mysql的資料檔案，./console up 自動生成)
dockerfiles/ (放置一些dockerfile，需要時重build自已的image使用)
logs/  (用來掛載及放置服務的紀錄)
service/ (放置擴充用的yml檔)
sites/ (專案的資夾，例如./create blog時，會建立在這個此目錄下)
samples/ (一些設定範本，例如: php.ini及一些額外的docker-compose yaml檔設定)
create (簡化的bash，用來快速的建立laravel的專案)
console(簡化的bash，用來快速使用各種docker-compose的命令。例如:./console mysql即可進入mysql)
docker-compose.yml (一個softlink，連結到不同的設定檔，例如:./console custom，即何將連結連到docker-compose-custom.yml)
</pre>
#### docker及docker-compose 版本要求

docker >= 18.02.0

docker-compose >= 1.19.0

#### 一、請先安裝docker
## 請使用最新版本的docker，至少應為18.02.0以上。

執行docker version確認docker的版本。
<pre>
$docker version
Client:
 Version:           18.06.0-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        0ffa825
 Built:             Wed Jul 18 19:05:26 2018
 OS/Arch:           darwin/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.06.0-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       0ffa825
  Built:            Wed Jul 18 19:13:46 2018
  OS/Arch:          linux/amd64
  Experimental:     true
</pre>
## 安裝docker的網址:
<pre>
Mac OS系統:
https://docs.docker.com/docker-for-mac/

Ubuntu:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

Windows 10:
https://docs.docker.com/docker-for-windows/install/
gitbash環境 (console及create需在gitbash環境執行，並且gitbash需可正確執行laravel installer!!)

</pre>

## 請確認您使用新版的docker-compose。

執行docker-compose version

大於等於

docker-compose version 1.19.0

## 安裝docker-compose網址
<pre>
https://docs.docker.com/compose/install/
</pre>

#### 二、例如:可用git clone下載這個repo，並進入dlaravel工作目錄。
<pre>
git clone https://github.com/DevinY/dlaravel.git
cd dlaravel
</pre>

#### 三、執行./create ['project name'] 建立開發專案
<pre>
例如: (第一次執行會自動下載所需的Image，需較長的時間)
./create test1

那麼就會建立出 http://test1.test 網站(本機測試用的外部無法存取)。
可以建立多個project站台

由於create的bash需有系統權修改/etc/hosts檔，./create的過程中會需要詢問您的系統密碼:
create指令、可在Mac OS、Linux及Windows 10的gitbash(Laravel installer)環境使用。
</pre>


#### 四、停止請在目錄下執行./console down
<pre>
注意事項: 這個只是拿來開發測試用的，Mysql的root是沒有密碼的。
你可能需要修改docker-compose.yml啟動時的TZ，目前設為Asia/Taipei
</pre>

#### 五、更新d-laravel bash程式及一些基本設定檔。
<pre>
git pull

在d-laravel的.gitignore已排除了會變動的區域了，例如: docker-compose.yml、docker-compse-custom.yml, sites專案資料夾等。
所以在dlaravel的目錄下，您可以透過git pull取得最新的版本及設定。
</pre>

#### 六、別名及功能(不需進入container即可執行container內的composer或artisan指令)

取得console別名
<pre>
 ./console alias
</pre>
把輸出結果，新增到~/.bash_profile，或是如果您用Z shell，新增到~/.zshrc檔案內。
在MacOs的系統預設不會有.bash_profile在家目錄中，你可以在終端機自己touch一個。
輸入: touch ~/.bash_profile

非必要項，自己有需要可新增或調整名稱。
<pre>
alias laravel='docker-compose exec -u dlaravel php /home/dlaravel/.composer/vendor/bin/laravel'
</pre>
使用dlaravel的身份執行container內的laravel installer

在Project內執行composer，例如ce dump
<pre>
alias ce="../../composer.sh"
</pre>

我們可以在自己的電腦加入別名，這樣就可不需進入container內執行php artisan指令了.
讓artisan的指令更簡潔，這理我直接將別名命名為a。
例如: a --version
<pre>
alias a="../../artisan.sh"
</pre>


<pre>
alias phpunit='docker-compose -f ../../docker-compose.yml exec -u dlaravel php $(basename ${PWD})/vendor/bin/phpunit -c $(basename ${PWD})/phpunit.xml'
</pre>
加入這個alias可以執行簡phpunit。
#### 其他
<pre>
./create [project名稱] 會建立及下載laravel，搞定一切設定，包含資料庫，
但如果是一個已存在的Project，只需有nginx的設定，應該怎麼做呢?

使用--host 即可修改系統的/etc/hosts檔，加入project的域名，如: project1.test。
./create --host [project名稱] 例如:./create --host project1

可以將已存在的Laravel專案移到sites資料夾內。

或是使用composer create-project指令建立Project.
例如使用手動指令手動建立Project，這裡用lumen示範。
./console exec，可用於執行php contaiener內的命令

./console exec composer create-project --prefer-dist laravel/lumen project1
</pre>
#### 調整設定檔的image切換
PHP: (OFFICIAL REPOSITORY重build符合Laravel環境)
https://hub.docker.com/r/deviny/fpm/tags/
<pre>
 mage: deviny/fpm:7.3.5
 image: deviny/fpm:7.2.18
 image: deviny/fpm:7.1.29
 image: deviny/fpm:5.6.39
</pre>

Nginx: (OFFICIAL REPOSITORY)
https://hub.docker.com/r/library/nginx/

Mysql: (OFFICIAL REPOSITORY)
https://hub.docker.com/_/mysql/

註: 原data資料夾已產生時，變更不同的mysql版本，在docker-compose.yml的設定檔內，
你需可能需調整資料庫夾data的名稱，確保新版的mysql image能正常運作。
例如:我將data設更為data_mysql8

<pre>
db:
  image: mysql:8
  略..
  volumes:
      - ./etc/mysql/my.cnf:/etc/mysql/my.cnf
      - ./data_mysql8:/var/lib/mysql
</pre>

#### 進階
如果您想重build自己php的fpm image版本。
例如下方建立了一個名為myfpm的image。
<pre>
cd dockerfiles/fpm/7.2
docker build -t myfpm .
</pre>

And then edit Your docker-compose.yml file.
然後，編輯docker-compose.yml檔，如下:
<pre>
 php:
  network_mode: "service:web"
  image: myfpm
</pre>

Docker指令及DevinY/dlaravel提供的./console的bash指令

|Docker官方指令   |簡易./console Bash指令| 說明|
|---|---|---|
| docker-compose pull  |./console pull   |抓最新的images   |
| docker-compose up -d  |./console up   |啟動container   |
| docker-compose down  |./console down  |停止container   |
| docker-compose ps或docker ps|./console ps  |查看docker-compose的process   |
| docker-compose exec -u dlaravel php bash   |./console  |進入php的container   |
| docker-compose exec php 指令  |./console exec 指令 |執行php container 指令，例如: ./console exec php -v|
| docker-compose exec db mysql   |./console mysql  |執行mysql   |
| docker-compose exec web nginx -s reload   |./console reload  |重載nginx設定   |
| docker-compose logs -f [SERVICE]   |./console logs  |看nginx的log，Ctrl+C停止 |
|   |./create [ProjectName]|建立一個project，並完成所有基本的環境設定   |
|   |例如: ./create test1  |例如: 這樣會建立一個http://test1.test的網站   |
|   |./console restart  |重啟container   |
|   |./console info  |查看目前可用的sites資料(這裡是查單的查詢sites資料夾)   |
|模式切換:|
|   |./console random  |container啟動時，使用隨機埠|
|   |./console normal  |使用本機port 80及127.0.0.1:3306|
|   |./console custom  |使用自己的docker-compose-custom.yml|
|下方: -f: 指定docker-compose設定檔。 up -d:啟動在背景執行。|
|docker-compose -f docker-compose-normal.yml up -d| |使用port 80及port 3306|
|docker-compose -f docker-compose-random.yml up -d| |指定隨機埠的啟動檔|

