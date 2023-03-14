### master启动方法
1. 在[master.py](../master/master.py)26行是workerlist列表，在每次启动前，都需要静态地配置worker的ip列表，列表的每一项是一个字典，字典的每一项分别代表worker的ip，监听的端口（默认是9999），state代表初始的状态，停用的话可以将其改为BUSY，或者将该行注释掉。需要指出的是，master本身也可以作为worker使用，配置方法见Readme.md中。
2. 进入master目录，`./run_master.sh`，没有权限的话就`sudo chmod u+x run_master.sh`
