import zmq

def print_dec(dec):
    for k,v in dec.items():
        print(k,v)

def getTaskSocket(my_ip_port,leader_ip_port,leader_time):
    context = zmq.Context()
    leader_ip_port_task = leader_ip_port.split(":")[0] + ":"
    leader_ip_port_task += str(int(leader_ip_port.split(":")[1])+1)
    if(my_ip_port == leader_ip_port):
        task_socket = context.socket(zmq.REP)
        task_socket.bind("tcp://%s"%leader_ip_port_task)
    else:
        task_socket = context.socket(zmq.REQ)
        task_socket.setsockopt(zmq.RCVTIMEO, leader_time)
        task_socket.connect("tcp://%s"%leader_ip_port_task)

    return task_socket

def leaderTask(task_port,my_ip_port):
    print("%s I'm the leader"%my_ip_port)
    while(True):
        task_port.recv_string()
        task_port.send_string(my_ip_port)

def machineTask(pub_sucket,sub_sucket,task_port,my_ip_port,dec,okay_time):
    print("%s I'm a normal machine"%my_ip_port)
    sub_sucket.setsockopt(zmq.RCVTIMEO, 0)
    while(True):
        task_port.send_string(my_ip_port)
        try :
            task_port.recv_string()
        except zmq.error.Again as e: #catch the exception comes from RCVTIMEO
            pub_sucket.send_string("Election Message " + dec[my_ip_port])
            sub_sucket.setsockopt(zmq.RCVTIMEO, okay_time)
            return # I find out that the leader is dead
        try:
            election = sub_sucket.recv_string()
        except zmq.error.Again as e: #catch the exception comes from RCVTIMEO
            continue
        if(election.split(" ")[0] == "Election Message" and election.split(" ")[1] > dec[my_ip_port]):
            sub_sucket.setsockopt(zmq.RCVTIMEO, okay_time)
            return # I got election message
            
        
