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

def leaderTask(task_socket,my_ip_port):
    print("%s I'm the leader"%my_ip_port)
    while(True):
        task_socket.recv_string()
        task_socket.send_string(my_ip_port)

def electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port, okay_time):
    
    recieved_ok = False
    
    pub_socket.send("%s %s" %("Election",my_ip_port))
    print("election message sent")
    try: 
        #check if i recieved election message from another machine
        recieved_message = sub_election_socket.recv()
        print("election message recieved")
        if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                pub_socket.send("%s %s" % (recieved_message.split(" ")[1], "Ok")) #reply with an ok message to that machine
                print("ok message sent to %s" %(recieved_message.split(" ")[1]))
    except  zmq.error.Again as e:
        dummy = 1

    try:
        #check if i recieved ok message from another machine
        recieved_message = sub_ok_socket.recv()
        recieved_ok = True
                  
    except zmq.error.Again as e:
        recieved_ok = False
    

    leader = ""
    if (recieved_ok == False):
        pub_socket.send("%s %s" %("Leader",my_ip_port))
        leader =  my_ip_port  

    else:
        msg = sub_leader_socket.recv()
        leader = (msg.split(" ")[1]) 

    while (True):
        try: 
            #check if i recieved election message from another machine
            recieved_message = sub_election_socket.recv()
            if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                    pub_socket.send("%s %s" % (recieved_message.split(" ")[1], "Ok")) #reply with an ok message to that machine
                    continue
        except  zmq.error.Again as e:
            break 

    sub_ok_socket.setsockopt(zmq.RCVTIMEO,0)
    while (True):
        try: 
            #check if i recieved election message from another machine
            recieved_message = sub_ok_socket.recv()
            continue
        except  zmq.error.Again as e:
            break                   
    sub_ok_socket.setsockopt(zmq.RCVTIMEO,okay_time)


    return leader
      

    #return "127.0.0.1:5555"        

def machineTask(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,task_socket,my_ip_port,okay_time):
    print("%s I'm a normal machine"%my_ip_port)
    #sub_sucket.setsockopt(zmq.RCVTIMEO, 0)
    while(True):
        try:
            recieved_election_msg = sub_election_socket.recv()
            if (dec[my_ip_port] > dec[recieved_election_msg.split(" ")[1]]):
                pub_socket.send("%s %s" % (recieved_election_msg.split(" ")[1], "Ok"))
                return electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)

        except:
            dummy = 1

        task_socket.send_string(my_ip_port)

        try :
            task_socket.recv_string()
        except zmq.error.Again as e:
            return electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)


            
        
