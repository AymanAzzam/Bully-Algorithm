import sys
import zmq
from zmq import EAGAIN
from utilities import *

# leader_time and okay_time in milliseconds

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
    #print_dec(dec)
    return dec,leader_time,okay_time

def connection(dec,my_ip_port,okay_time):
    context = zmq.Context()
    pub_sucket = context.socket(zmq.PUB)
    sub_sucket = context.socket(zmq.SUB)

    pub_sucket.bind("tcp://%s"%my_ip_port)
    sub_sucket.subscribe("")
    sub_sucket.setsockopt(zmq.RCVTIMEO, okay_time)
    for k,v in dec.items():
        if(k != my_ip_port):
            sub_sucket.connect("tcp://%s"%k)
    
    return pub_sucket,sub_sucket

def electLeader(pub_sucket,sub_sucket,my_ip_port):
    #return the leader_ip_port
    return "127.0.0.1:5555"

def main():
    my_ip_port = sys.argv[1]
    
    dec,leader_time,okay_time = configuration()
   
    pub_sucket,sub_sucket = connection(dec,my_ip_port,okay_time)
   
    while(True):
        leader_ip_port = electLeader(pub_sucket,sub_sucket,my_ip_port)
   
        task_port = getTaskSocket(my_ip_port,leader_ip_port,leader_time)

        if(my_ip_port == leader_ip_port):
            leaderTask(task_port,my_ip_port)
        else:
            #the machine should return if it knows that the leader is dead
            machineTask(pub_sucket,sub_sucket,task_port,my_ip_port,dec,okay_time)

main()
