
###
 # @Descripttion: Online Judge
 # @version: ^_^
 # @Author: Jingbin Yang
 # @Date: 2021-09-30 15:25:52
 # @LastEditors: Jingbin Yang
 # @LastEditTime: 2021-10-01 18:51:00
### 
# Change the sources to tsinghua mirror, which is specified by sources.list
# The origin sources.list is saved to sources.list.bak
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp aptSource/sources.list /etc/apt/
# Copy the key-pair to the worker
sudo mkdir -p /root/.ssh
sudo cp RSAKeyPair/id_rsa /root/.ssh/
sudo cp RSAKeyPair/id_rsa.pub /root/.ssh/
sudo chmod 600 /root/.ssh/id_rsa

# Update and upgrade
yes | sudo apt update
# yes | sudo apt upgrade

yes | sudo apt install mininet
yes | sudo apt install ethtool arptables iptables curl p7zip-full vim python make gcc
yes | sudo apt install redis-server python-celery-common

python pipSource/get-pip.py
export PATH="~/.local/bin/:$PATH"
# echo "export PATH=~/.local/bin/:$PATH" >> ~/.bashrc
# source ~/.bashrc

if [ ! -d "~/.pip" ];then
    mkdir ~/.pip
fi
cp pipSource/pip.conf ~/.pip/pip.conf


pip install redis celery
