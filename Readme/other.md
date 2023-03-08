1. 安装解压工具7z，`sudo apt install p7zip-full`
2. 换清华源ubuntu 22.04`sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak`备份并`sudo cp aptSource/sources.list /etc/apt/`（如果有需要的话）
3. 安装tmux，`sudo apt install tmux`，用于在shell关闭之后服务仍然运行，也可以使用nohup，但是感觉tmux挺好用
4. 后面的实验会用到traceroute，如果系统不自带请自行安装