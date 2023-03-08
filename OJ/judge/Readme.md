# 说明

-----------------
1. 安装对应环境
    - 网络工具 `sudo apt install ethtool arptables iptables`
    - 仿真工具 `sudo apt install mininet`
    - 分布式工具 `pip install celery`
    - 存储工具 `pip install redis`，若下载失败则采用`pip3`
    - 解压工具 `sudo apt install p7zip-full`
----------------

2. 单点测试环境是否安装完全（**强烈推荐**进行本步骤）
    - 解压`FIX.zip`,进入`FIX`目录后,用`python2`执行`main.py`，即`python main.py`,使用`python2/python`取决于自己的配置。
    - 若最后终端打印出`json`, 如
    ```javascript
    {
        "id": "1", 
        "homeworkId": "1", 
        "statusCode": 200, 
        "scores": {
            "LossTopo": {
                "testCase": 5, 
                "passedCase": 5
            }, 
            "GeneralTopo": {
                "testCase": 5, 
                "passedCase": 5
            }
        }
    }
    ```
    则代表成功，重点关注`statusCode`是否为`200`，本压缩包仅供你测试，没有其他用。
-------------------
3. 配置分布式所需要的环境
    - 2.1 `ssh`权限相关
        - 为测试方便，将 `ssh localhost` 设置为密钥登录。
        - 方法：`ssh-keygen` 生成本地密钥对，`ssh-copy-id -i ~/.ssh/id_rsa.pub yourUserName@localhost` ,输入密码即可
    - 2.2 `sudo`权限相关
        - 为便于发布给`worker`命令,需要将`sudo`免命令使用，此处sudo是必须的，因为启动`mininet`需要`sudo`
        - 方法：`root`下修改`/etc/sudoers`,如果未成功,可以第一次手动输入,后面很长一段时间不用输密码。
    - 2.2 `redis` 相关
        - 打开redis配置文件 `sudo vim /etc/redis/redis.conf`
        - 确保 `127.0.0.1 xxx` 这一行没被注释掉，本地测试用（默认没被注释掉）
        - 确保端口号为`6379`（默认值）,如果改为其他，则在`yjb/celery_app/celeryconfig.py`中进行对应的更改
        - 可设置密码为`123456`,如果改为其他，则在`yjb/celery_app/celeryconfig.py`进行对应的更改
        - 上述配置如有更改，则需要`redis-cli shutdown`关闭`redis`之后，`sudo redis-server /etc/redis/redis.conf`应用配置文件，然后在sunGiveMeJson.py中第22行进行相应的更改
        - 如果你用了`redis`的话，那这一块咱们可能需要好好商量一下，觉得这块很虚
4. 尝试对接......
    - <p1 id = "1">这是一个为了跳转的标签</p1>
    - 在`yjb`目录下开3个终端
    - 终端1：`celery -A celery_app worker --loglevel=debug`,此为运行在本地的`worker`，负责接受并完成master分配的任务，并返回一个`json`给`master`，你不用和它对接
    - 终端2：`python sunGiveMeJson.py`,此为`master`,负责接受`sunPythonDemo.py`的命令并分发给worker并将`worker`返回结果`post`上去，现为`print`用来测试，因为不知道post地址，这个需要你去掉注释生效。另外，对于本端口，未知原因只能`ctrl z`挂起，然后你可以`lsof -i:7777`或`ps aux | grep sunGiveMeJson.py`查看此`pid`，`kill -9 pid`杀死即可，记得加`-9`。
    - 终端3：`python sunPythonDemo.py`,此为我写的用来给`master`传递作业路径等信息的`pythonDemo`,以下为对此文件的详细说明
    - `sunPythonDemo.py`详细说明：提供了`python`下利用`socket`给`sunGiveMeJson.py`发送json信息的一种实现方式,你可以自己写一个`sunJavaDemo.java`尝试对接一下，成功后将`sunJavaDemo.java`嵌入你的代码中。`(ip,port) = (127.0.0.1,7777)`
----------------------
5. 一言一图以蔽之
    ```javascript
    {
        "id": "1", 
        "homeworkId": "1", 
        "path": "zipPath"
    }
    ```
    `path`为绝对路径，`id/homeworkid`目前随便传


# 增加的功能
1. 改变json格式为你要求的格式，如下所示：
```json
{
    'code': 500,
    'message': '就不为空',
	'data' : {
        "fileId": "1", 
        "expId": "1", 
        "status": "200", 
        "statusDescr": "没有makefile"
    }
}
```
其中状态码及其描述解释如下，为防止出现编码问题，目前全部采用***英文***
```python
status = "200"
    statusDescr = "Decompress fails" #解压失败
    statusDescr = "No makefile" #没有makefile
    statusDescr = "Compile fails" # 编译失败
status = "300"
    statusDescr = "Run result: GeneralTopo tests pass 4/5; LossTopo tests pass 3/5" #两种拓扑结构分别测试结果
status = "100"
    statusDescr = "Run result: GeneralTopo tests pass 5/5; LossTopo tests pass 5/5" #全部正确
```
2. 为方便你测试，增加了`testZipSrc`目录，可以直接在前端上传。其中
    - `allPassed.zip`: 可以正常通过
    - `compileFails.zip`: 编译失败
    - `noMakefile.zip`: 没有makefile
-------------------------------





# 从这儿开始看(可先看带<u>***ATTENTION***</u>的优化项）

增加的功能 2021/8/11
-------------------------------
1. 规范了文件目录便于后增加作业种类及后续维护
2. <u>***ATTENTION***</u>提示信息改为中文，便于阅读，解决了编码问题
3. <u>***ATTENTION***</u>使用了自己的www目录，大大降低了上传的压缩包大小，加快了处理速度，目前测试样例1M内即可
4. ***TO BE CONTINUED......***
-------------------------------
增加的功能 2021/8/12
-------------------------------
1. <u>***ATTENTION***</u>增加了`userId`便于存放文件
2. 在得出成绩之后会删除之前上传的zip，只保留最后一次提交的代码，无论通过与否
3. 在[ sunGiveMeJson.py ](sunGiveMeJson.py)的26-27行显示了保存最后一次提交作业的路径，目前为[ archive ](archive)，如无必要则不用改，改了之后还得塞进去标准standard代码，直接用就行
4. 运行`python killPort.py`可直接根据`socket`开的端口杀死`ctrl z`后的[ sunGiveMeJson.py ](sunGiveMeJson.py)
5. <u>***ATTENTION***</u>增加了全局配置文件，位于[ sunConnectyy/conf/globalConf.py ](./conf/globalConf.py)，可在此处修改`socket`端口和`redis`配置等信息，后续为管理方便还会加进去其他的配置变量如状态码
6. 准备写个emmm，不写了，写个屁
7. ***TO BE CONTINUED......***
-------------------------------
增加的功能 2021/8/13
------------------------------
1. <u>***ATTENTION***</u>解决了`sudo`需要输入密码的问题。解决方法如下（`ubuntu18.04`，用户名为`yangxiaomao`）：
    - `whereis mn`命令查看`mn(mininet)`命令所在目录，应该是在`/usr/bin/mn`
    - `su`后输入密码进入`root`模式
    - 修改`sudoer`文件，`vim /etc/sudoers`
    - 小心改，在`root`下一行增加
        ```shell
        yangxiaomao ALL=(ALL:ALL) NOPASSWD:ALL
        ```
        如果已经有自己的用户行，那么加一个`NOPASSWD`改成这个样子就行，代表给予`yangxiaomao`用户执行所有命令的权限并加入`sudo`组
    - ***重点***：在`sudoer`文件随后的几行，有
    ```shell
    # Allow members of group sudo to execute any command
    %sudo   ALL=(ALL:ALL) ALL
    ```
    将下面%sudo这一行改为
    ```shell
    %sudo   ALL=(ALL:ALL) NOPASSWD:/usr/bin/mn #推荐
    ```
    意为在`sudo`组的用户在执行`/usr/bin/mn`命令时不需要输入密码，若改为
    ```shell
    %sudo   ALL=(ALL:ALL) NOPASSWD:ALL #不推荐
    ```
    意为在sudo组的用户在执行所有命令时不需要输入密码，但是不安全，可以执行`mn`即可。
    网上的方法只是把`yangxiaomao`加入`sudo`组，但是`sudo`组本身并不具有免密权限，现提升了`sudo`组的权限，可放心。
    - 检验方法：命令行输入`sudo mn`，若不需要输入密码即操作成功
2. <u>***ATTENTION***</u>支持`expId = 1/2/3/4/5/6/7/8`，`userId`、`fileId`随意，接收格式为
    ```json
    {
        "fileId":"1",
        "expId":"3",
        "userId":"6",
        "filePath":"/home/yangxiaomao/src/allPassed.zip"           
    }
    ```
    返回格式为
    ```json
    {
        "fileId": "1", 
        "expId": "3", 
        "userId": "6", 
        "status": "100", 
        "statusDescr": "常规拓扑通过：5/5; 丢包拓扑通过：5/5", 
        "test": "5,5,5,5"
    }
    ```
3. <u>***ATTENTION***</u>全局配置文件[ sunConnectyy/conf/globalConf.py ](./conf/globalConf.py)中，增加了参数`RM_ORIGIN`，如果为`True`，那么会删除原始文件，否则不会，设置此参数的意义在于为了方便前后端`debug`，否则一闪而过根本不知道到底存下来了没有
4. 增加了几个测试文件位于[ ./testZipSrc ](./testZipSrc)，便于查重，其中`1.zip,2.zip,3.zip,4.zip`都跑不过（md学生的都过不了服了，不过足够你测试查重了），剩余的三个文件和之前一样如其名所示，全通过/无Makefile/编译失败。同时我把全通过的代码放到了每次作业的`standardCode`目录中，如[ sunConnectyy/archive/1/standardCode/ ](./archive/1/standardCode/)，这样可以查重测试，但是毕竟不是框架代码，查重率和真实值会有所差距。 
5. 辛苦了^__^mua~
6. 将存储路径加入配置文件[ sunConnectyy/conf/globalConf.py ](./conf/globalConf.py)
7. 可以自动建立`CODELIBPATH`目录，可以自动建立每次作业的目录，可以自动建立每次作业目录下面每个学生的目录，简而言之，一开始啥都不需要，只需要再[ sunConnectyy/conf/globalConf.py ](./conf/globalConf.py)中修改`CODELIBCODE`即可
8. 为配合查重，在每次作业目录下移动生成standard目录，同时在每次作业目录的同级目录生成code和result的目录
9. 怕你还得找开终端的方法，点击[ 此处 ](#1)可跳转至使用方法
10. ***TO BE CONTINED......***
-------------------------------
增加的功能 2021/8/14
-------------------------------
1. 规范了存档目录结构，让id1下直接是代码文件，而不是嵌套的目录，便于查重模块的运行
2. 更改了`code`和`result`目录的位置为每次实验对应
3. 不足：`standard`目录目录结构得自己放进去，这个提前自己放进去就ok，但是必须有人交作业才能生成各个目录，才能有放`standard`代码的地方



