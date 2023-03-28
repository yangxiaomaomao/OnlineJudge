### master上需要执行
1. 安装ssh，`sudo apt install openssh-server`
### worker上需要执行
1. 为了worker可以自动地从master下载文件并进行判题，我们需要将worker的公钥放到master上，方法如下。
2. worker上`sudo ssh-keygen`生成密钥对
3. worker上`sudo ssh-copy-id -i yangxiaomao@192.168.0.230`,此处yangxiaomao为master用户名，192.168.0.230位master内网地址（这里假定worker和master处于同一局域网内）
4. 这里要注意，需要用sudo执行上述操作，原因是由于worker的判题需要用到mininet，而mininet不管是cli还是api的调用都需要sudo权限，所以执行worker的脚本`./run_worker.sh`的时候需要用sudo，而这个时候main.py里面的scp也就变成了是sudo在执行，便需要sudo免密登录master所以需要传root用户的密钥到master
5. 另外，由于自动判题的需要，需要将判题机器执行sudo命令时变为免密操作。将用户加入sudo组`sudo usermod -aG sudo yangxiaomao`，添加免密`sudo vim /etc/sudoers`在其中加入`yangxiaomao ALL=(ALL:ALL) NOPASSWD:ALL`记得将yangxiaomao改成自己用户名，%后面没有空格。另外还需要格外记住，在设置sudo免密的时候，确保这句话写在靠下的位置，否则其所属于的组的设置可能会覆盖掉这一行的设置，如
```
yangxiaomao ALL=(ALL:ALL) NOPASSWD:ALL
%sudo ALL=(ALL:ALL) ALL
```
groups一下可以看到yangxiaomao属于sudo组和yangxiaomao组，但是下面的那一行会覆盖掉上面一行的设置，从而导致yangxiaomao还是需要免密。可以直接让sudo组免密，也可以把那句话写到%sudo...下面一行

### tips
1. 可以在~/.ssh/config文件中配置如下,可以方便登录217 worker，`ssh w217`
```
Host w217
    HostName 192.168.0.217
    User yangxiaomao
```