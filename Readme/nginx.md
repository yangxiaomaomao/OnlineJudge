1. 安装：`sudo apt install nginx`
2. 设置nginx自启动：`sudo systemctl enable nginx`
3. 配置文件(其中需要修改的地方用`TO FIX`标注)
- 修改`nginx.conf`的三处路径（主要是修改home路径的用户名）
- 修改ip地址，如果本机测试则填127.0.0.1:80；如果直接上线则填192.168.0.230:80,192.168.0.230是master的内网地址
4. 将nginx的配置文件移动到nginx配置文件的位置`sudo cp ~/OnlineJudge/OJ/nginx/nginx.conf /etc/nginx/conf.d/`，并使用`sudo systemctl restart nginx`重启nginx服务
5. 浏览器访问localhost或上线的ip，出现`Welcome to nginx!......`界面即成功。（默认80端口）