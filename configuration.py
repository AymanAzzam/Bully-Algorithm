
def configuration():
    dec = {}
    f = open("config.txt","r")
    leader_time = int(f.readline())
    okay_time = int(f.readline())
    machines_num = int(f.readline())

    while(machines_num>0):
        ip_port_pri = (f.readline())
        dec[ip_port_pri.split(" ")[0]] = int(ip_port_pri.split(" ")[1])
        machines_num -= 1
    return dec,leader_time,okay_time
