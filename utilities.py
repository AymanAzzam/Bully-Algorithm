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
    sub_election_socket.setsockopt(zmq.RCVTIMEO,0)

    while (True)
        try: 
            #check if i recieved election message from another machine
            
            recieved_message = sub_election_socket.recv()
            print("election message recieved")
            if (dec[my_ip_port] > dec[leader_dead_msg.split(" ")[1]]):
                    pub_socket.send("%s %s" % ("Ok",recieved_message.split(" ")[1])) #reply with an ok message to that machine
                    print("ok message sent to %s" %(recieved_message.split(" ")[1]))
                    
        except  zmq.error.Again as e:
                break

    try:
        #check if i recieved ok message from another machine
        sub_ok_socket.setsockopt(zmq.RCVTIMEO,okay_time) # 10 to be changed
        recieved_message = sub_ok_socket.recv()
        recieved_ok = True
                  
    except zmq.error.Again as e:
        recieved_ok = False

     
                 

    if (recieved_ok == False):
        pub_socket.send("%s %s" %("Leader",my_ip_port))
        return my_ip_port  

    else:
        sub_leader_socket.setsockopt(zmq.RCVTIMEO,-1)
        msg = sub_leader_socket.recv()
        return (msg.split(" ")[1]) 


      

    #return "127.0.0.1:5555"        

def machineTask(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,task_socket,my_ip_port,okay_time):
    print("%s I'm a normal machine"%my_ip_port)
    #sub_sucket.setsockopt(zmq.RCVTIMEO, 0)
    while(True):
        try:
            recieved_election_msg = sub_election_socket.recv()
            if (dec[my_ip_port] > dec[leader_dead_msg.split(" ")[1]]):
                electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)
        except:

        task_socket.send_string(my_ip_port)

        try :
            task_socket.recv_string()
        except zmq.error.Again as e:
            electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)


            
        
