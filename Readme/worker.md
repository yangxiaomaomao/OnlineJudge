### worker的部署方法
1. 在[main.py](../worker/main.py)的180-181行，如果此时worker同时是master，那么使用`returnData["ip"] = "127.0.0.1"`，否则一般用`returnData["ip"] = str(socket.gethostbyname(socket.gethostname()))`
2. 在[main.py](../worker/main.py)的174行和189行，修改ip为master的ip。（`os.system("scp -r yangxiaomao@192.168.0.230:%s ." % filePath)`和`sendBackToMaster("192.168.0.230", 4320, returnData)`）
2. 进入worker目录，`./run_worker.sh`，没有权限的话就`sudo chmod u+x run_worker.sh`