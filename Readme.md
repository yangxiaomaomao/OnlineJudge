# 本系统是一个用于国科大计算机网络课的判题系统，需要和固定的代码框架做适配，只使用本框架作用不大

## 准备工作
### master准备工作
1. [安装小工具](./Readme/other.md)
2. [存档工作](./Readme/archive.md)
4. [安装并配置docker](./Readme/docker.md)
5. [安装nginx前端并配置](./Readme/nginx.md)
6. [安装java后端](./Readme/springBoot.md)
7. [安装数据库](./Readme/database.md)
8. [ssh配置](./Readme/ssh.md)
9. [master](./Readme/master.md)介绍

### worker准备工作
1. 将worker目录放导worker机器的家目录（其他地方也行不过没必要）
2. [ssh配置](./Readme/ssh.md)
3. [安装mininets](./Readme/mininet.md)

## 启动方法
### master
1. 启动nginx：`sudo systemctl restart nginx`(每次修改nginx.conf都最好重启一下)
2. 在[tmux](./Readme/tmux.md)中启动springBoot后端：`java -jar xx.jar`，xxx.jar是编译好的包，目前叫做OnlineJudge.jar，位置在OJ/springBoot
3. 在[tmux](./Readme/tmux.md)中启动数据库：进入OJ/database并且执行`docker-compose up -d`
4. 在[tmux](./Readme/tmux.md)中[启动master](./Readme/master.md)

### worker
1. 在[tmux](./Readme/tmux.md)中[启动worker](./Readme/worker.md)

## 模块介绍
1. 