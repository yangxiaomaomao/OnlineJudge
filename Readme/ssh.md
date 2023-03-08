0. 安装ssh，`sudo apt install openssh-server`
1. 为了worker可以自动地从master下载文件并进行判题，我们需要将worker的公钥放到master上，方法如下。
2. worker上`sudo ssh-keygen`生成密钥对
3. worker上`sudo ssh-copy-id -i yangxiaomao@192.168.0.230`,此处yangxiaomao为master用户名，192.168.0.230位master内网地址（这里假定worker和master处于同一局域网内）
4. 这里要注意，需要用sudo执行上述操作，原因是由于worker的判题需要用到mininet，而mininet不管是cli还是api的调用都需要sudo权限，所以执行worker的脚本`./run_worker.sh`的时候需要用sudo，而这个时候main.py里面的scp也就变成了是sudo在执行，便需要sudo免密登录master所以需要传root用户的密钥到master