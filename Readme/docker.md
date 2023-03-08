1. 安装docker：`sudo apt install docker`,`sudo apt install docker.io`
2. 安装docker-compose：`sudo apt install docker-compose`
2. 检查是否有docker组：`cat /etc/group | grep docker`,如果有就下一步,否则`sudo groupadd docker`
3. 将用户加入到docker组：`sudo usermod -aG sudo $USER`或`sudo gpasswd -a $USER docker`
4. 重启docker：`sudo systemctl restart docker`
5. 检测是否成功：`docker ps`，如果还是没有权限，是因为没有切换到docker组，此时执行`newgrp docker`.