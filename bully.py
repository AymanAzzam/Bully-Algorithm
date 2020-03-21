import sys
import zmq

# leader_time and okay_time in milliseconds

def print_dec(dec):
    for k,v in dec.items():
        print(k,v)

def configuration():
    dec = {}
    f = open("config.txt","r")
    leader_time = int(f.readline())
    okay_time = int(f.readline())
    machines_num = int(f.readline())

    while(machines_num>0):
        ip_port_pri = (f.readline())
        dec[ip_port_pri.split(" ")[0]] = ip_port_pri.split(" ")[1]
        machines_num -= 1
    print_dec(dec)
    return dec,leader_time,okay_time

def connection(my_ip_port,dec):
    context = zmq.Context()
    pub_sucket = context.socket(zmq.PUB)
    sub_sucket = context.socket(zmq.SUB)

    pub_sucket.bind("tcp://%s"%my_ip_port)
    sub_sucket.subscribe("")
    for k,v in dec.items():
        if(k != my_ip_port):
            sub_sucket.connect("tcp://%s"%k)
    
    return pub_sucket,sub_sucket

def electLeader(my_ip_port):
    return 0

def task(my_ip_port,leader_ip_port):
    if(leader_ip_port == my_ip_port):
        print("I'm the Leader, my_ip_port is %s"%my_ip_port)
    else:
        print("I'm normal machine, my_ip_port is %s"%my_ip_port)

def main():
    my_ip_port = sys.argv[1]
    dec,leader_time,okay_time = configuration()
    pub_sucket,sub_sucket = connection(my_ip_port,dec)
    leader_ip_port = electLeader(my_ip_port)

main()
