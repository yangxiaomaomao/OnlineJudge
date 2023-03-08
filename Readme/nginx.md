1. 安装：`sudo apt install nginx`
2. 设置nginx自启动：`sudo systemctl enable nginx`
3. 配置文件：修改`nginx.conf`的三处路径（主要是修改home路径的用户名）以及ip为本服务器ip(其中需要修改的地方用`TO FIX`标注),将nginx的配置文件移动到nginx配置文件的位置`sudo cp ~/OnlineJudge/OJ/nginx/nginx.conf /etc/nginx/conf.d/`，并使用`sudo systemctl restart nginx`重启nginx服务
4. 浏览器访问localhost，出现`Welcome to nginx!......`界面即成功。（默认80端口）