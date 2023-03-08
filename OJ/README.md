<!--
 * @Author: your name
 * @Date: 2021-09-29 15:33:57
 * @LastEditTime: 2021-09-30 14:26:50
 * @LastEditors: your name
 * @Description: In User Settings Edit
 * @FilePath: \deployment\README.md
-->
# Deployment目录详解

运行整个项目前，在根路径下新建archive目录作为代码库

## database

存放使用到的数据库：

*   mysql：存放学生的数据
*   redis：存放登录验证码
*   celery_redis：用于判题模块

封装在了docker里。进入该目录，使用命令`docker-compose up -d`即可启动

## nginx

前端文件存放位置。

使用命令`npm run build`编译前端代码后，将dist目录下的内容拷贝至该目录。

log目录存放运行时的日志。

将nginx的配置文件`nginx.conf`拷贝至`/etc/nginx/conf.d/`下面

## springBoot

后端项目打包为jar包后放置在此位置。

使用命令`java -jar xx.jar`启动，注意需要java版本11

log目录存放运行时的日志。

## judge

判题模块，用于和后端通信并分发作业至虚拟机运行。

TODO：让杨景彬写

## archive

代码库，保存学生提交的作业以及查重结果。

其结构为：

    archive
    	1	// 目录名为实验的id
    	...
    	16
    		id1		// 表示用户id为1的学生，提交作业时自动生成
    		id2
    		code	// 存放查重的对比文件，，需要提前手动创建好
    		result	// 存放查重结果，，需要提前手动创建好
    		standard	// 存放查重用的框架代码，，需要提前放置好
    	zip	// 临时性保存文件的目录，需要提前手动创建好

## run.py

还未写，python脚本，运行直接启动整个项目

首先创建`/archive`目录，并赋予全部的写权限（a+w）。

# 部署步骤

将deployment目录放置在主目录下

将archive目录移动到根目录下，即`/archive`，并添加写权限`sudo chmod a+w /archive`

将nginx的配置文件移动到`/etc/nginx/conf.d/nginx.conf`，并修改其中的三处路径（主要是修改home路径的用户名）以及ip为本服务器ip，使用`sudo systemctl restart nginx`重启nginx服务



后端可以直接运行，`java -jar OnlineJudge.jar`



数据库可直接运行，进入目录`~/deployment/database` 下执行命令：`docker-compose up -d`



（注意，如果不在本机上判题，则不需要执行这两步操作）判题模块需要首先设置root权限名，使用root身份修改`/etc/sudoers`文件：

1.  为当前用户添加root身份：`yangxiaomao ALL=(ALL:ALL) NOPASSWD:ALL`

2.  免密执行mininet，`%sudo   ALL=(ALL:ALL) NOPASSWD:/usr/bin/mn`

使用终端（建议使用tmux）运行`deployment/judge`目录下的master.py文件

使用终端运行命令（需要先启动docker中的数据库）`celery -A celery_app worker --loglevel=debug`

