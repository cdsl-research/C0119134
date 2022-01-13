import sys
#filename = "nginxconf.txt"

def readfile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        txt = f.readlines()
    return txt
            
def writefile(filename, txt):
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(txt)
        
    
if __name__ == '__main__':
    args = sys.argv
    filename = args[1]
    timeout = args[2]
    txt = readfile(filename)
    for i in range(len(txt)):
        x = txt[i].find("keepalive_timeout")
        if x>=0:
            num = i
            break
    line = " "*x+"keepalive_timeout  "+timeout+";\n"
    txt[num] = line
    writefile(filename, txt)