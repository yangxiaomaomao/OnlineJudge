def rewriteStandard(file,myIP,yourIP):
    with open(file,"r") as f1:
        fileContent = f1.read()
    with open(file,"w") as f2:
        f2.write(fileContent.replace('my_ip_here', myIP).replace('your_ip_here', yourIP))
    
        
rewriteStandard("standard.html","10.2","8963")