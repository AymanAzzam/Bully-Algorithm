dec = {}

my_ip_port = ""

leader_ip_port = ""

time_limit = int ## in seconds

def print_dec():
    for k,v in dec.items():
        print(k,v)

def init():
    f = open("config.txt","r")
    time_limit = int(f.readline())
    machines_num = int(f.readline())
    for i in range(0,machines_num):
        ip_port_pri = (f.readline())
        dec[ip_port_pri.split(" ")[0]] = ip_port_pri.split(" ")[1]
    print_dec()

def electLeader():
    return
def main():
    init()
    electLeader()

main()