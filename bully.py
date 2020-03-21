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

def connection():
    context = zmq.Context()
    pub_sucket = context.socket(zmq.PUB)
    sub_sucket = context.socket(zmq.SUB)

    pub_sucket.bind("tcp://%s"%my_ip_port)
    sub_sucket.subscribe("")
    return pub_sucket,sub_sucket

def electLeader():
    return

def main():
    dec,leader_time,okay_time = configuration()
    pub_sucket,sub_sucket = connection()
    electLeader()

main()
