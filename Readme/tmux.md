### tmux用于在shell退出后服务仍然存在，常见的命令如下
1. tmux new -s master（建立一个名字叫做master的tmux终端）
2. tmux a -t master（进入master终端）
3. 在tmux终端里面ctrl + b然后ctrl + d退出终端
4. 在tmux终端里面ctrl + b然后ctrl + w可以选择终端
5. tmux ls查看已经启动的终端
6. 建立`~/.tmux.conf`并在其中输入`set -g mouse on`可以开启tmux终端翻页