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
        dec[ip_port_pri.split(" ")[0]] = int(ip_port_pri.split(" ")[1])
        machines_num -= 1
    #print_dec(dec)
    return dec,leader_time,okay_time

def connection(dec,my_ip_port,okay_time):
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    sub_election_socket = context.socket(zmq.SUB)
    sub_ok_socket = context.socket(zmq.SUB)
    sub_leader_socket = context.socket(zmq.SUB)

    pub_socket.bind("tcp://%s"%my_ip_port)
    sub_election_socket.subscribe("Election")
    sub_ok_socket.subscribe(my_ip_port)
    sub_leader_socket.subscribe("Leader")


    sub_election_socket.setsockopt(zmq.RCVTIMEO,0)
    sub_ok_socket.setsockopt(zmq.RCVTIMEO,okay_time)
    sub_leader_socket.setsockopt(zmq.RCVTIMEO,-1)
   
    for k,v in dec.items():
        if(k != my_ip_port):
            sub_election_socket.connect("tcp://%s"%k)
            sub_ok_socket.connect("tcp://%s"%k)
            sub_leader_socket.connect("tcp://%s"%k)
    
    return pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket



def main():
    
    my_ip_port = sys.argv[1]
    
    dec,leader_time,okay_time = configuration()
   
    pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket = connection(dec,my_ip_port,okay_time)
   
    while(True):
        leader_ip_port = electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)
   
        task_socket = getTaskSocket(my_ip_port,leader_ip_port,leader_time)

        if(my_ip_port == leader_ip_port):
            leaderTask(task_socket,my_ip_port,pub_socket,sub_election_socket)
        else:
            #the machine should return if it knows that the leader is dead
            leader_ip_port = machineTask(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,task_socket,my_ip_port,okay_time)

main()
