<!--
 * @Descripttion: Online Judge
 * @version: ^_^
 * @Author: Jingbin Yang
 * @Date: 2021-10-03 14:01:19
 * @LastEditors: Jingbin Yang
 * @LastEditTime: 2021-10-08 15:11:39
-->
# worker
adduser yangxiaomao
/etc/sudoers中
加%userGroupName ALL=(ALL:ALL) NOPASSWD:ALL
加userName ALL=(ALL:ALL) ALL

1. chmod 777 *.sh
2. sudo su设置root密码，避免改出乱子
3. 修改master的IP，在judge/conf/globalConf.py
4. task.py中修改masterAddr为master，"userName@IP"
5. sudo ssh-keygen, sudo ssh-copy-id yangxiaomao@192.168.3.43 

# master 
1. 修改nginx/nginx.conf中的路径
2. /etc/ssh/sshd_config开启密钥登录
- 2.1 #StrictModes yes  ->  StrictModes no
- 2.2 #AuthorizedKeysFile .ssh/authorized_keys -> AuthorizedKeysFile .ssh/authorized_keys
- 2.3 #PubkeyAuthentication yes -> PubkeyAuthentication yes
3. start_nginx    = "sudo systemctl restart nginx"
start_judger   = "java -jar springBoot/OnlineJudge.jar" 
start_database = "cd database && sudo docker-compose up -d"
start_master   = "cd judge && python master.py"
4. flower监控celery flower --address=0.0.0.0 --port=5555 --broker=redis://localhost:6380/0


