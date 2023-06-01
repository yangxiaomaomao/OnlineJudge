import sys
import os
import time
import json
sys.path.append("..")
from tools.tools import fillInInfo


DEBUG = 1

# use this function may cause sunmission to loop forever 
def execCmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text  

if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "ip_lookup"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
        
    info = {}
    
    scores = {}

    os.system("chmod 775 %s" % exec_file)

    execCmd("./%s" % exec_file)
    
    time.sleep(2)
    
    os.system("sudo pkill %s" % exec_file)
    
    with open("res.txt","r") as f:
        res = f.readline().split(",")
    basic_pass = res[0]
    basic_time = res[1]
    advanced_pass = res[2]
    advanced_time = res[3]
    
    scores["basic_pass_test"] = (basic_pass == 1)
    scores["advanced_pass_test"] = (advanced_pass == 1)
    scores["advanced_efficiency_test"] = (basic_pass == 1) and \
                                         (advanced_pass == 1) and \
                                         (basic_time > 2 * advanced_time) and \
                                         (advanced_time < 16000)
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
