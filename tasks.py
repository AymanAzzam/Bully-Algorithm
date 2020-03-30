#import zmq
from bully import *

def getTaskSocket(my_ip_port,leader_ip_port,leader_time):
    context = zmq.Context()
    leader_ip_port_task = leader_ip_port.split(":")[0] + ":"
    leader_ip_port_task += str(int(leader_ip_port.split(":")[1])+1)
    if(my_ip_port == leader_ip_port):
        task_socket = context.socket(zmq.REP)
        task_socket.setsockopt(zmq.RCVTIMEO, 0)
        task_socket.bind("tcp://%s"%leader_ip_port_task)
    else:
        task_socket = context.socket(zmq.REQ)
        task_socket.setsockopt(zmq.RCVTIMEO, leader_time)
        task_socket.connect("tcp://%s"%leader_ip_port_task)
    return task_socket

def machineTask(dec,push_socket,push_okay_socket,pull_socket,task_socket,my_ip_port,leader_ip_port,okay_time):
    print("%s I'm a normal machine and I'm doing my task \n"%my_ip_port)
    while(True):
        out = machineCheckElection(dec,task_socket,push_socket,push_okay_socket,pull_socket,my_ip_port,leader_ip_port)
        if(out != 0):   # The leader changed
            return out

        try:
            task_socket.send_string(my_ip_port)
            task_socket.recv_string()
        except zmq.error.Again as e:
            print("I found that the leader died \n")
            print("************************************************ \n")
            return electLeader(dec,push_socket,push_okay_socket,pull_socket,my_ip_port,okay_time)


def leaderTask(dec,task_socket,my_ip_port,push_socket,pull_socket):
    print("%s I'm the leader and I'm doing my task \n"%my_ip_port)
    while(True):
        try:
            task_socket.recv_string()
            task_socket.send_string(my_ip_port)
        except zmq.error.Again as e:
            dummy = 1

        while(True):
            out = leaderCheckElection(dec,push_socket,pull_socket,my_ip_port)
            if(out == 0):   # i didn't receive anything
                break
            elif(out != 1): # i received Leader message from priority higher than me
                return out
