#DevinYlaravel(d-laravel)
您是否還不是很了解nginx的主機設定?  讓DevinY/laravel幫助您，快速進入Laravel的本機開發環境。

類似於官網的Valet，可同時執行多個 *.dev的開發測試的網站。

d-laravel使用dockr-compose的微服務架構，

還可自訂docker-compose-custom.yml快速創建出自己的開發環境。

###為什麼用d-laravel
話說，在自己在MacOS上編譯php及架設環境並不是一件容易的事情。

而Apple對於php版本的更新也不是那麼快， 如果我想在MacOS跑不同的PHP或新版PHP似乎讓事情變的有點麻煩。

Docker跟Vagrant比起來，docker的啟動速度是秒級的，比起Vagrant的VM的分鐘級的啟動速度，快很多。

而Laravel官方的Valet，我的使用經驗上也是要裝一堆東西，DnsMasq及Caddy，對於我的錯亂中的Mac，只會更加錯亂@@

吃了我的port 80搞半天移不太掉，最後官方的移除指令valet uninstall才搞定。

總而言之，最後我覺的docker才是解決之道，不用再被環境所困。

因為我是Mac的使用者，

所以，就建立了./conosle及./create這兩個bash指令，

來幫助我快速建立Laravel在Mac OS上的本機測試環境。

建立Project使用，基本上您只要會下方四種指令就搞定啦 
<pre>
./create test1  (建立test1.dev)
./console down或./console up (啟用及停用container)
./console restart    (./console down再./console up)
</pre>


####一、請先安裝docker-for-mac
<pre><code>
https://docs.docker.com/docker-for-mac/
<br/>
</code></pre>

####二、例如用git clone這個repo，並進入laravel資料夾，然後執行：./console pull。
<pre><code>
git clone https://github.com/DevinY/laravel.git
cd laravel
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


####四、停止請在目錄下執行./console down
<pre><code>
注意事項: 這個只是拿來開發測試用的，Mysql的root是沒有密碼的。
你可能需要修改docker-compose.yml啟動時的TZ，目前設為Asia/Taipei
</code></pre>

####五、更新
<pre><code>
cd laravel-dev
git pull
</code></pre>

Docker指令及DevinY/laravel提供的./console的bash指令

|Docker官方指令   |./console Bash指令| 說明|
|---|---|---|
| docker-compose pull  |./console pull   |抓最新的images   |
| docker-compose up -d  |./console up   |啟動container   |
| docker-compose down  |./console down  |停止container   |
| docker-compose ps或docker ps|./console ps  |查看docker-compose的process   |
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
