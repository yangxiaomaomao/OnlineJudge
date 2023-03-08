
###
 # @Descripttion: Online Judge
 # @version: ^_^
 # @Author: Jingbin Yang
 # @Date: 2021-09-30 15:53:01
 # @LastEditors: Jingbin Yang
 # @LastEditTime: 2021-10-01 13:53:29
### 
# Change the sources to tsinghua mirror, which is specified by sources.list
# The origin sources.list is saved to sources.list.bak

# #Create the directory to save the file temporily
sudo mkdir -p /archive
sudo mkdir -p /archive/zip
sudo chmod 777 -R /archive

# ssh
mkdir -p ~/.ssh
touch ~/.ssh/authorized_keys
cat RSAKeyPair/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys

sudo chmod 777 -R *
# # apt source
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp aptSource/sources.list /etc/apt/

# Update and upgrade
sudo apt update
sudo apt upgrade #NOT RECOMMEND

# Install curl
yes | sudo apt install curl
# Install celery
yes | sudo apt install python-celery-common
# Install ssh
yes | sudo apt install openssh-server
# Install docker
echo "Install docker......"
curl -sSL https://get.daocloud.io/docker | sh
echo "Finish installing docker"

# Install docker-compose
echo "Downloadinging docker-compose"
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
echo "Installing docker-compose"
sudo chmod +x /usr/local/bin/docker-compose
echo "Finish installing docker-compose"

# #Install jdk11
echo "Installing jdk11, this may take a long time...You can read a short novel or others to spend the boring time....."
yes | sudo apt install openjdk-11-jdk
echo "Finally we finish installing jdk11, happy!"

# #Install Nginx
echo "Installing Nginx"
yes | sudo apt install nginx
echo "Finish installing Nginx"

# # nginx
sudo cp nginx/nginx.conf /etc/nginx/conf.d/

yes | sudo apt install python

python pipSource/get-pip.py
export PATH="~/.local/bin/:$PATH"
# echo "export PATH=~/.local/bin/:$PATH" >> ~/.bashrc
# source ~/.bashrc

if [ ! -d "~/.pip" ];then
    mkdir -p ~/.pip
fi
cp pipSource/pip.conf ~/.pip/pip.conf
