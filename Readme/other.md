1. 安装解压工具7z，`sudo apt install p7zip-full`
2. 换清华源ubuntu 22.04`sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak`备份并`sudo cp aptSource/sources.list /etc/apt/`（如果有需要的话）
3. 安装tmux，`sudo apt install tmux`，用于在shell关闭之后服务仍然运行，也可以使用nohup，但是感觉tmux挺好用
4. 将系统语言改为英文，因为判题的时候可能会从终端读取输出结果，所以中文的话会出问题，`vim ~/.profile` 在最后一行添加`LANG="EN_US.UTF-8"`，然后`source ~/.profile`，终端`locale`可以查看，另外这个时候要注意，tmux需要重新启动，否则tmux内部的语言还是没有换回来，图方便的话直接在tmux终端内部`source ~/.profile`即可
4. 后面的实验会用到traceroute，如果系统不自带请自行安装