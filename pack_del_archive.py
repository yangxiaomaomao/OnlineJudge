import os
import sys

## del archive of the last term's students
## !!ATTENTION, make sure the path string is not none, or your system will be down
def del_archive():
    print("Pay attention to the cmd you will execute")
    sys.exit(0)
    dir_list = [str(i) for i in range(13,25)]
    print(dir_list)
    #sys.exit(0)
    for dir in dir_list:
        hw_path = os.path.join("/archive", dir)
        print("rm -rf %s/*" % hw_path)
        assert(hw_path != "")
        assert(hw_path != " ")
        os.system("rm -rf %s/*" % hw_path)
    

## pack archives at the end of a term
def pack_archive():
    dir_name = "/archive"
    home_path = "/home/yangxiaomao"
    os.system("sudo cp -r %s %s" % (dir_name,home_path))
    os.system("sudo chmod 777 -R %s/archive")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pack_del_archive.py OPERATION, OPERATION supports \"del\" or \"pack\"")
        sys.exit(0)
        
    if sys.argv[1] == "del":
        del_archive()
    elif sys.argv[1] == "pack":
        pack_archive()
    else:
        print("Only pack and del is supported")
        sys.exit(0)