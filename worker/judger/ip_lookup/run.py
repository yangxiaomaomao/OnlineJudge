import sys
import os
import time
import json

DEBUG = 0

if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "ip_lookup"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
        
    info = {}

    os.system("chmod 775 %s" % exec_file)
    os.system("")
    
    scores = {
        "simple_topo": simpleOspfTopoTest(exec_file),
        "switch_topo": switchOspfTopoTest(exec_file)
    }
    if not DEBUG:
        os.remove(exec_file)

    scores["simple_ping"] = scores["simple_topo"][0]
    scores["unlink_ping"] = scores["simple_topo"][1]
    del scores["simple_topo"]

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
