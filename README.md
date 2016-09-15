#laravel
不是很了解nginx的主機設定嗎? 

這個repo幫助你，快速進入Laravel的簡易開發環境。

用docker-compose在MacOS下建立PHP-FPM、MySQL及nginx的簡易環境。

類似於Valet同，可同時執行多個 *.dev的開發測試的網站。

在dockr-compose的微服務架構，您也可以自訂docker-compose-custom.yml快速創建出自己的開發環境。

####一、請先安裝docker-for-mac
<pre><code>
https://docs.docker.com/docker-for-mac/
<br/>
</code></pre>

####二、下載這個repo，並進入laravel-dev資料夾，然後執行：。
<pre><code>
./console pull
第一次執行會花較久的時間從dockhub上，下載docker-compose所需要的images.
<br/>
</code></pre>

####三、執行./create ['project name'] 建立開發專案
<pre><code>
例如:
./create test1
那麼就會建立出 http://test1.dev 網站(本機測試用的外部無法存取)。
可以建立多個project站台

需有系統權修改/etc/hosts檔，./create的過程中會需要詢問您的系統密碼:
目前只可在Mac OS上使用。
<br/>
</code></pre>


四、停止請在目錄下執行./console down
<pre><code>
注意事項: 這個只是拿來開發測試用的，Mysql的root是沒有密碼的。
你可能需要修改docker-compose.yml啟動時的TZ，目前設為Asia/Taipei
</code></pre>

五、透過別名我們可以在任何地方執行console
例如，也可以把./console alias的別名加入到~/.bash_profile中，永久生效
<pre><code>
顯示別名sample
./console alias
建立別名
source `./console alias`
</code></pre>

六、更新
<pre><code>
cd laravel-dev
git pull
</code></pre>

Docker指令及Larave-dev提供的Bash

|Docker官方指令   |簡易console bash   | 說明|
|---|---|---|
| docker-compose pull  |./console pull   |抓最新的images   |
| docker-compose up -d  |./console up   |啟動container   |
| docker-compose down  |./console down  |停止container   |
| docker-compose ps   |./console ps  |查看docker-compose的process   |
| docker-compose exec php bash   |./console  |進入php的container   |
| docker-compose exec db mysql   |./console mysql  |執行mysql   |
| docker-compose exec web nginx -s reload   |./console reload  |從載nginx設定   |
|   |./create [ProjectName]|建立一個project，並完成所有機本的環境設定   |
|   |例如: ./create test1  |例如: 這樣會建立一個http://test1.dev的網站   |
|   |./console restart  |重啟container   |
|   |./console info  |查看目前可用的sites資料(這裡是查單的查詢sites資料夾)   |
|模式切換:|
|   |./console random  |container啟動時，使用隨機埠|
|   |./console mode1  |使用本機port 80及127.0.0.1:3306|
|   |./console custom  |使用自己的docker-compose-custom.yml|
|下方相當於，透過./console mode1設定模式後，執行./console up:|
|docker-compose -f docker-compose-mode1.yml up -d| |使用port 80及port 3306|
|docker-compose -f docker-compose-random.yml up -d| |指定隨機埠的啟動檔|
