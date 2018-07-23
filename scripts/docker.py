# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import re
import platform
import locale
import fileinput
from shutil import copyfile
system = platform.system()
major = sys.version_info[0]
basepath = os.getcwd()
def e(v):
    print(v)

def get_projects_count():
    count = 0
    for file_or_dir in os.listdir("{}/sites".format(basepath)):
        if(os.path.isdir("sites/{}".format(file_or_dir))):
            count+=1
    return count

def pull():
    command=dockerCompose()+["pull"]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    e(output)

def node():
    command="docker run --rm -v {}/sites:/sites -w /sites -ti node bash".format(basepath).split();
    subprocess.call(command)

def get_sites():
    sites=[]
    for file_or_dir in os.listdir("{}/sites".format(basepath)):
        if(os.path.isdir("sites/{}".format(file_or_dir))):
            sites.append(file_or_dir)
    return sites

def run(command):
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    return proc.stdout.read()

#檢測dot_env中使用的installer
def dot_env_install():
    fname = "{}/.env".format(basepath)
    if(os.path.isfile(fname)): 
        lines = open(fname, "r").readlines()
        for line in lines:
            obj = re.search("^LARAVEL_INSTALLER=(.+)", line, re.I | re.M)
            if(obj):
                value = remove_quotes(obj.group(1))
                return value
    return "container"

#找出.env擋中定義的服務
def dot_env_services():
    default_compose=["docker-compose","-f","{}/docker-compose.yml".format(basepath)]
    fname = "{}/.env".format(basepath)
    if(os.path.isfile(fname)): 
        lines = open(fname, "r").readlines()
    else:
        return default_compose

    env_command = []
    for line in lines:
        obj = re.search("^DOCKER_SERVICES=(.+)", line, re.I | re.M)
        if(obj):
            services = remove_quotes(obj.group(1))
            services = re.sub("(\\s+)", " ", services)
            services = services.split(' ')
            for service in services:
                env_command += ["-f"]+["{}/{}".format(basepath,service)]
    
    if(len(env_command) > 0):
        return ["docker-compose"]+env_command
    else:
        return default_compose 

def dockerCompose():
    command =  dot_env_services()
    return command;

def ps():
    command=dockerCompose()+["ps"]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    e(output)

def check_link_or_create():
    if os.path.isfile(basepath+"/docker-compose.yml") == False:
        src=basepath+"/docker-compose-normal.yml";
        dst=basepath+"/docker-compose.yml";
        os.symlink(src, dst)

def up():
    check_link_or_create()
    command=dockerCompose()+["up","-d"]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    e(output)

def down():
    check_link_or_create()
    command=dockerCompose()+["down"]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    e(output)

def restart():
    down()
    up()

def get_container_name(service):
    #docker-compose ps db
    command=dockerCompose()+["ps", service]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    result = re.sub("(.+\\n-+\\n)(.+)\\n", "\\2", output)
    result = re.sub("^(.*?)\\s.+", "\\1", result)
    result = re.sub("(.+)\\n?", "\\1", result)
    if(re.search(".+_\\w+_\\d", result, re.I | re.M)):
        return result
    else:
        return ""

def is_running():
    command=dockerCompose()+["ps", "web"]

def db_ports():
    container_name = get_container_name("db")
    if(container_name == "" ):
        print("db is not running.")
        return

    command=["docker","inspect","--format='{{(index (index .NetworkSettings.Ports \"3306/tcp\") 0).HostPort}}'", container_name]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    print("DB:")
    e("host:{}".format(output))

def web_ports():
    container_name = get_container_name("web")
    if(container_name == "" ):
        print("web is not running.")
        return

    command=["docker","inspect","--format='{{(index (index .NetworkSettings.Ports \"80/tcp\") 0).HostPort}}'", container_name]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    http_port = int(remove_quotes(proc.stdout.read()))
    print("WEB:")
    for file_or_dir in os.listdir("{}/sites".format(basepath)):
        if(os.path.isdir("sites/{}".format(file_or_dir))):
            if(http_port==80):
               print("http://{}.test".format(file_or_dir))
            else:
               print("http://{}.test:{}".format(file_or_dir, http_port))

def info():
      db_ports()
      web_ports()

def ext():
    output = run(dockerCompose()+["exec","php","php","-i"])
    obj = re.search("^extension_dir(.+)", output, re.I | re.M)
    lines = obj.group(1).split('=>')
    extension_dir=lines[1]
    e(run(dockerCompose()+["exec","php","ls",extension_dir.strip()]))

def reload():
    output = run(dockerCompose()+["exec","web","nginx","-s","reload"]).decode('utf-8')
    e(output)

def remove_quotes(v):
    return re.sub("'", "", v.decode('utf8'))

def normal():
    try:
        os.symlink("{}/docker-compose-normal.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    except:
        os.remove("{}/docker-compose.yml".format(basepath))
        os.symlink("{}/docker-compose-normal.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    restart();

def random():
    try:
        os.symlink("{}/docker-compose-normal.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    except:
        os.remove("{}/docker-compose.yml".format(basepath))
        os.symlink("{}/docker-compose-random.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    restart();

def custom():
    try:
        os.symlink("{}/docker-compose-custom.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    except:
        os.remove("{}/docker-compose.yml".format(basepath))
        os.symlink("{}/docker-compose-custom.yml".format(basepath),"{}/docker-compose.yml".format(basepath))
    restart();

def execute(args):
    command = dockerCompose()+args 
    subprocess.call(command)

def logs(service=[]):
    if(len(service)==0):
            command = dockerCompose()+["logs"]
    else:
            command = dockerCompose()+["logs"]+service
    try:
            subprocess.call(command)
    except:
        pass

def mysql():
    command = dockerCompose()+["exec", "db", "env"]
    output = run(command)
    obj=re.search("MYSQL_ROOT_PASSWORD=(.*)",output, re.I | re.M)
    #password = obj.group(1)
    if(obj):
        command = dockerCompose()+["exec","db","mysql","-uroot","-p"]
    else:
        command = dockerCompose()+["exec","db","mysql","-uroot"]
    subprocess.call(command)

def secure():
    if(system == "Darwin"):
        projects = get_projects_count();
        if(projects == 0):
            msg = """No Projects are found, you can create one by following command.
For example as below:
./create [project name]
or
To manually create new default project:
mkdir -p sites/default/public;touch sites/default/public/index.php"""
            print(msg)
            exit()
        copyfile("{}/etc/default-ssl.sample".format(basepath), "{}/etc/default-ssl.conf".format(basepath))
        copyfile("{}/etc/v3.sample".format(basepath), "{}/etc/v3.ext".format(basepath))

        count=0
        with open("{}/etc/v3.ext".format(basepath), 'a') as v3_file:
            for project_name in get_sites():
                count+=1
                v3_file.write("DNS.{}=www.{}.test\n".format(count, project_name))
                count+=1
                v3_file.write("DNS.{}={}.test\n".format(count, project_name))

        command = ["security","find-certificate","-c","\"dlaravel.test\"",
        "-a","-Z","|","sudo","|","awk" ,"'/SHA-1/{system(\"security delete-certificate -Z \"$NF)}'"]
        subprocess.call(command)

        command = ["openssl","req","-new","-newkey","rsa:2048","-sha256",
        "-days","3650","-nodes","-x509",
        "-keyout","{}/etc/ssl/cert.key".format(basepath),
        "-out","{}/etc/ssl/cert.crt".format(basepath),
        "-config","{}/etc/v3.ext".format(basepath),"-extensions","v3_req"]
        subprocess.call(command)

        command = ["sudo","security","add-trusted-cert","-d","-r","trustRoot","-k","/Library/Keychains/System.keychain","{}/etc/ssl/cert.crt".format(basepath)]
        subprocess.call(command)

        reload()

    else:
        print("This feature for OSX user only.")

def link():
    command=["ls","-l","{}/docker-compose.yml".format(basepath)]
    e(run(command))

def chowner():
    if(system=="Linux"):
        whoami = run(["whoami"]).strip("\n")

        dlaravel_uid = run(["id","-u",whoami])
        dlaravel_gid = run(["id","-g",whoami])
        command = dockerCompose()+["exec","php","usermod","-u",dlaravel_uid.strip('\n'),"dlaravel"]
        subprocess.call(command)
        command = dockerCompose()+["exec","php","groupmod","-g",dlaravel_gid.strip('\n'),"dlaravel"]
        subprocess.call(command)
        command = dockerCompose()+["exec","php","chown","-R",dlaravel_uid.strip('\n'),"/home/dlaravel"]
        subprocess.call(command)
        msg ="""You have to commit your php fpm image, and restart container.
Example: docker commit 67306ecd0879 deviny/fpm:7.1.9
./console restart"""
        print(msg)


def clear():
    if(major==3):
        ans = input("Would You like to stop / remove all Docker containers?(y/n)")
    else:
        ans = raw_input("Would You like to stop / remove all Docker containers?(y/n)")
    if(ans.lower() == 'y'):
        command = ["docker","ps","-qa"]
        containers = run(command).decode('utf-8').split('\n')
        for container_id in containers:
            if(container_id!=""):
                command = ["docker","rm","-f",container_id]
                subprocess.call(command)
    else:
        exit()

def help():
    l=locale.getdefaultlocale()[0]
    msg="""
 usage: {} [<option>]
 options:
     """.format(sys.argv[0])
    print(msg)
    if(l=="zh_TW"):
        msg="""   up : 建立並啟動container。
   down : 停止並移除container。
   restart : 停止再啟動down and up，不明怪問題時應該有用
   ps : Lists Contaienrs. (docker-compose -f ${base_path}/docker-compose.yml ps)
   alias : 顯示consle的別名指令
   logs : container service的log, 用Ctrl+C中斷
   info : 列出web及db在host的連接埠。
   mysql : 快速進入mysql
   link : 目前docker-compose 連結的設定檔
   secure: 加入https設定檔
   normal : 變更docker-compose連結，讓docker使用標準連結埠，80:443:3306
   random : 變更docker-compose連結，讓docker啟用隨機的連接埠，可用./console ps查看
   custom : 變更docker-compose連結，產生或使用自定的設定檔
   exec : 執行php container內的命令，例如: ./console exec php php -v
   reload : 重載nginx的設定.
   node: 會執行node容器，並且掛載/sites資料夾。
   ext: 列出目前fpm可用的php exteinsions，自訂檔名新增.ini檔到etc/php下即可啟用哦。
   chowner: D-Laravel的使用者uid及gid在容器內預設為1000，在linux環境中，您可能需要調整dlaravel的uid與gid與您的目前使用者相同
   clear : 移除所有docker ps -a 所有停止的Container!!包含您自己過去創建的所有停止的container哦!!
   ./console : 進入php container內
   version : 顯示目前的版本.
   """
        print(msg)
    else:
        msg="""   up : Run containers in the background.
   down : Stop and remove containers, networks.
   restart : Restart services.
   ps : Lists Contaienrs. (docker-compose -f ${base_path}/docker-compose.yml ps)
   alias : Display console's alias setting.
   logs : service's log, ctrl+c to stop.
   info : list webs and port of database.
   mysql : Enter mysql interactive mode.
   link : Display current link of docker-compose file.
   secure: Add self-signed ceftifiecate, to enable https support.
   normal : change docker-compose.yal link to docker-compose-normal.yml, for using ports 80:443:3306
   random : change docker-compose.yml link to docker-compose-random.yml，for using random ports，you can check issue ./console ps
   custom : change docker-compose.yml link link to docker-compose-custom.yml， for custom purpose.
   exec : exec php container's command， for example: ./console exec php php -v
   reload : nginx reload config file.
   node: run nodejs container, and mount /sites folder.
   ext: list php extensions.
   chowner: D-Laravel users uid and gid are 1000 in container, in the linux environment, you may need to adjust D-Laravel uid and gid with your current user the same.
   clear : Remove all your containers that listed by docker ps -a !!
   ./console : Enter php container.
   version : Display current version.
   
   I'm not native speaker in English, please feel free to send me a PR to fix the help.
   """
        print(msg)

def version():
    file = open("{}/etc/dlaravel-release".format(basepath), "r") 
    e(file.read())

def alias():
    print("alias c={}/console".format(basepath))

def dlaravel_new(parameter):
     value=dot_env_install()
     if(os.path.isdir("{}/sites/{}".format(basepath,parameter))):
         print("The sites/{} folder exists.".format(parameter))
         exit()
     if(value=="host"):
         print("Run laravel installer on host: laravel new {}".format(parameter))
         command=["laravel","new","sites/{}".format(parameter)]
         print(command)
         subprocess.call(command)
     else:
         print("Run laravel installer in container: laravel new {}".format(parameter))
         command=dockerCompose()+["exec","-u","dlaravel","php","/home/dlaravel/.composer/vendor/bin/laravel","new",parameter]
         print(command)
         subprocess.call(command)

def dlaravel_config(parameter):
    print("Update the sites/{}/.env file of the project.".format(parameter))
    #更新.env設定連線
    command=dockerCompose()+["exec","-u","dlaravel","php","sed","-i","s/DB_HOST=127.0.0.1/DB_HOST=db/","/var/www/html/{}/.env".format(parameter)]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    command=dockerCompose()+["exec","-u","dlaravel","php","sed","-i","s/DB_DATABASE=homestead/DB_DATABASE={}/".format(parameter),"/var/www/html/{}/.env".format(parameter)]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    command=dockerCompose()+["exec","-u","dlaravel","php","sed","-i","s/DB_USERNAME=homestead/DB_USERNAME={}/".format(parameter),"/var/www/html/{}/.env".format(parameter)]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    command=dockerCompose()+["exec","-u","dlaravel","php","sed","-i","s/DB_PASSWORD=secret/DB_PASSWORD={}/".format(parameter),"/var/www/html/{}/.env".format(parameter)]
    proc = subprocess.Popen(command ,shell=False, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')

def create_host(project):
    fname="/etc/hosts"
    lines = open(fname, "r").readlines()
    found = 0
    for line in lines:
        if(re.search("^(127.0.0.1)\\s+(www.)?(.+).test$", line, re.I | re.M)):
            #移除斷行
            result = re.sub("(^127.0.0.1)\\s+(www.)?(.+).test", "\\3", line.rstrip())
            #print("[{}]".format(result))
            if(result == project):
                found = 1
    if(found == 0):
         command=["sudo","python","{}/scripts/update_hosts.py".format(basepath), project]
         subprocess.call(command)

def create_db(project):
         command=["docker-compose","exec","db","mysql","-e","CREATE DATABASE IF NOT EXISTS `{}`".format(project)]
         subprocess.call(command)
         command=["docker-compose","exec","db","mysql","-e","CREATE USER IF NOT EXISTS \"{}\"".format(project,project)]
         subprocess.call(command)
         command=["docker-compose","exec","db","mysql","-e","SET PASSWORD FOR `{}`=\"{}\"".format(project,project)]
         subprocess.call(command)
         command=["docker-compose","exec","db","mysql","-e","GRANT ALL ON `{}`.* TO \"{}\"".format(project,project)]
         subprocess.call(command)
         command=["docker-compose","exec","db","mysql","-e","FLUSH PRIVILEGES"]
         subprocess.call(command)


