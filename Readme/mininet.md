由于mininet从不知道什么时候开始支持python3，所以我们最新版本的OJ框架试图跟上，不可避免地可能出现问题。如果想用python3的调用mininet的API，需要从源码安装mininet
1. `git clone https://github.com/mininet/mininet.git`（没有git自行安装）
2. 如果`python --version`显示是python3，那么直接install，否则进入mininet目录执行`PYTHON=python3 util/install.sh -fnv`（在mininet的INSTALL文件里面有所说明），过程中会自动从github安装openflow，如果不科学上网可能会卡死，自己改install.sh从gitee下载也行
3. 判断是否安装成功：`python3`后`import mininet`，没报错就成功