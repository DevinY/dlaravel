#D-Laravel

D-Laravel採用了dockr-compose的微服務架構，

經由簡易的console及create bash，幫您快速建立出基本的Laravel開發環境。

主要包含，nginx(網頁服務)、php-fpm(php)及mysql(資料庫)，

使用D-Laravel，代表了，我們的Mac系統，不再需要安裝mysql，nginx及php-fpm，

我只要透過docker container來建立起獨立的容器空間即可。

可自訂docker-compose-custom.yml快速創建出自己的開發環境。

###為什麼用D-Laravel

Docker跟Vagrant比起來，docker的啟動速度是秒級的，

可模擬不同的資料庫環境。

可同時開啟多個不同的測試站台。

可以自行控制使用php的版本，必要時自己重編docker php-fpm image。

使用dokcer官方的php image，建立Laravel所需的執行環境。

對於不了解docker指令的使用者，提供簡易的Bash進行docker-compose指令快速操作。

可使用最新的PHP在Mac OS上執行。

可以快速協助設定self-signed憑證。

用docker聽起來，好像比較潮。:p
<pre>
./console help (幫助，console參數用法。)
./create test1  (建立test1.dev)
./console down或./console up (啟用及停用container)
./console restart    (./console down再./console up)
`./console alias`  
(打./console指令太長了嗎，上方指令可暫時用c代表./console，所以執行後，輸入:c info、c up或c down..即可執行。)
./console alias    (印出console的別名範本，自行加到.bashrc或.zshrc永久生效)

產生HTTPS加密的域名設定及自我簽署的憑證，
為了讓Chrome正常顯示，需要把生成的域名存入系統鑰匙圈中，因此會詢問系統密碼(MacOS only)。
./console secure test1 
(https://test1.dev 網址)
</pre>

####主要目錄結構
<pre>
etc/   (nginx、php.ini及mysql的相關設定檔)
data/  (mysql的資料檔案，./console up 自動生成)
sites/ (專案的資夾，./create test1時，會建立在這個此目錄下)
create (簡化的bash，用來快速的建立laravel的專案)
console(簡化的bash，用來快速使用各種docker-compose的命令。例如:./console mysql即可進入mysql)
docker-compose.yml (一個softlink，連結到不同的設定檔，例如:./console custom，即何將連結連到docker-compose-custom.yml)
</pre>

####一、請先安裝docker-for-mac
<pre>
https://docs.docker.com/docker-for-mac/
</pre>

####二、例如用git clone這個repo，並進入laravel資料夾，然後執行：./console pull。
<pre>
git clone https://github.com/DevinY/dlaravel.git
cd dlaravel

下方pull的動作是可以略過，啟動時，會依docker-compose.yml的設定自動下載所需的images。
./console pull
當第一次執行會花較久的時間從dockhub上，下載docker-compose所需要的images.
</pre>

####三、執行./create ['project name'] 建立開發專案
<pre>
例如:
./create test1
那麼就會建立出 http://test1.dev 網站(本機測試用的外部無法存取)。
可以建立多個project站台

需有系統權修改/etc/hosts檔，./create的過程中會需要詢問您的系統密碼:
目前只可在Mac OS上使用。
</pre>


####四、停止請在目錄下執行./console down
<pre>
注意事項: 這個只是拿來開發測試用的，Mysql的root是沒有密碼的。
你可能需要修改docker-compose.yml啟動時的TZ，目前設為Asia/Taipei
</pre>

####五、更新d-laravel bash程式及一些基本設定檔。
<pre>
git pull

在d-laravel的.gitignore已排除了會變動的區域了，例如: docker-compose.yml、docker-compse-custom.yml, sites專案資料夾等。
所以在dlaravel的目錄下，您可以透過git pull取得最新的版本及設定。
</pre>

####其他
<pre>
./create [project名稱] 會建立及下載laravel，搞定一切設定，包含資料庫，
但如果是一個已存在的Project，只需有nginx的設定，應該怎麼做呢?

使用--conf產生nginx的網頁伺服器設定檔。(會建立在dlaravel/etc資料夾下)
./create --conf [project名稱] 例如:project1

可以將已存在的Laravel專案移到sites資料夾內。

或是手動方式執行composer create-project (非預設的版本等)
例如使用手動指令手動建立Project，這裡用lumen示範。
./console exec，可用於執行php contaiener內的命令

./console exec composer create-project --prefer-dist laravel/lumen project1
</pre>

####進階
Dlaravel，完全採用官方版本的image進行設定，使用上大家可以放心。
但由於PHP的官方dokcer image並沒有Laravel所需的擴充套件，
因此dlaravel的fpm由image是由的php dokcer官方的image重build出來的。

如果您想學習或重build自己php的fpm image版本，例如擴展php的功能，
那麼可到下方連結參考，就可了解dlaravel的fpm image怎麼來的，及如何用docker重build一個自己的phpfpm image。
https://github.com/DevinY/fpm/blob/master/README.md

Docker指令及DevinY/dlaravel提供的./console的bash指令

|Docker官方指令   |簡易./console Bash指令| 說明|
|---|---|---|
| docker-compose pull  |./console pull   |抓最新的images   |
| docker-compose up -d  |./console up   |啟動container   |
| docker-compose down  |./console down  |停止container   |
| docker-compose ps或docker ps|./console ps  |查看docker-compose的process   |
| docker-compose exec php sudo -u dlaravel bash   |./console  |進入php的container   |
| docker-compose exec php 指令  |./console exec 指令 |執行php container 指令，例如: ./console exec php -v|
| docker-compose exec db mysql   |./console mysql  |執行mysql   |
| docker-compose exec web nginx -s reload   |./console reload  |從載nginx設定   |
| docker-compose logs -f [SERVICE]   |./console logs  |看nginx的log，Ctrl+C停止 |
|   |./create [ProjectName]|建立一個project，並完成所有基本的環境設定   |
|   |例如: ./create test1  |例如: 這樣會建立一個http://test1.dev的網站   |
|   |./console restart  |重啟container   |
|   |./console info  |查看目前可用的sites資料(這裡是查單的查詢sites資料夾)   |
|模式切換:|
|   |./console random  |container啟動時，使用隨機埠|
|   |./console normal  |使用本機port 80及127.0.0.1:3306|
|   |./console custom  |使用自己的docker-compose-custom.yml|
|下方: -f: 指定docker-compose設定檔。 up -d:啟動在背景執行。|
|docker-compose -f docker-compose-normal.yml up -d| |使用port 80及port 3306|
|docker-compose -f docker-compose-random.yml up -d| |指定隨機埠的啟動檔|
