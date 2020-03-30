from configuration import *
from connection import *
from tasks import *


def main():
    my_ip_port = sys.argv[1]
    
    dec,leader_time,okay_time = configuration()
   
    push_socket,pull_socket = setConnection(dec,my_ip_port,okay_time)

    clearSocketBuffer(pull_socket)
    
    leader_ip_port = electLeader(dec,push_socket,pull_socket,my_ip_port,okay_time)

    while(True):

        task_socket = getTaskSocket(my_ip_port,leader_ip_port,leader_time)

        if(my_ip_port == leader_ip_port):
            leader_ip_port =leaderTask(dec,task_socket,my_ip_port,push_socket,pull_socket)
        else:
            leader_ip_port = machineTask(dec,push_socket,pull_socket,task_socket,my_ip_port,leader_ip_port,okay_time)

main()
