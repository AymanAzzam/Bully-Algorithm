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
        task_socket.setsockopt(zmq.RCVTIMEO, 0)
        task_socket.bind("tcp://%s"%leader_ip_port_task)
    else:
        task_socket = context.socket(zmq.REQ)
        task_socket.setsockopt(zmq.RCVTIMEO, leader_time)
        task_socket.connect("tcp://%s"%leader_ip_port_task)

    return task_socket

def leaderTask(task_socket,my_ip_port,pub_socket,sub_election_socket):
    print("%s I'm the leader \n"%my_ip_port)
    while(True):
        try:
            task_socket.recv_string()
            task_socket.send_string(my_ip_port)
            #print("Leader Received Task and replied on it")
        except zmq.error.Again as e:
            dummy = 1

        while(True):
            try:
                recieved_message = sub_election_socket.recv_string()
                print("Leader Got Election message from Machine %s \n"%recieved_message.split(" ")[1])
                pub_socket.send_string("%s %s" % (recieved_message.split(" ")[1], my_ip_port))
            except zmq.error.Again as e:
                break

def electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port, okay_time):
    
    recieved_ok = False
    
    pub_socket.send_string("%s %s" %("Election",my_ip_port))
    print("Election message sent \n")
    try: 
        #check if i recieved election message from another machine
        recieved_message = sub_election_socket.recv_string()
        print("Election message recieved \n")
        if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                pub_socket.send_string("%s %s" % (recieved_message.split(" ")[1], "Ok")) #reply with an ok message to that machine
                print("ok message sent to %s \n" %(recieved_message.split(" ")[1]))
    except  zmq.error.Again as e:
        dummy = 1
    
    print("Checking Okay message \n")
    try:
        #check if i recieved ok message from another machine
        recieved_message = sub_ok_socket.recv_string()
        if (recieved_message.split(" ")[1] != "Ok"):
            print("I received message from the leader \n")
            return recieved_message.split(" ")[1] 
        print("I received okay message from %s \n"%recieved_message.split(" ")[0])
        recieved_ok = True
    except zmq.error.Again as e:
        print("I didn't receive okay message \n")
        recieved_ok = False
    

    leader = ""
    if (recieved_ok == False):
        pub_socket.send_string("%s %s" %("Leader",my_ip_port))
        leader =  my_ip_port  

    else:
        msg = sub_leader_socket.recv_string()
        leader = (msg.split(" ")[1]) 

    while (True):
        try: 
            #check if i recieved election message from another machine
            recieved_message = sub_election_socket.recv_string()
            if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                    pub_socket.send_string("%s %s" % (recieved_message.split(" ")[1], "Ok")) #reply with an ok message to that machine
                    continue
        except  zmq.error.Again as e:
            break 

    sub_ok_socket.setsockopt(zmq.RCVTIMEO,0)
    while (True):
        try: 
            #check if i recieved election message from another machine
            recieved_message = sub_ok_socket.recv_string()
            continue
        except  zmq.error.Again as e:
            break                   
    sub_ok_socket.setsockopt(zmq.RCVTIMEO,okay_time)


    return leader       

def machineTask(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,task_socket,my_ip_port,okay_time):
    print("%s I'm a normal machine \n"%my_ip_port)
    while(True):
        try:
            recieved_election_msg = sub_election_socket.recv_string()
            task_socket.send_string("is leader alive")
            try:
                task_socket.recv_string()
            except zmq.error.Again as e:
                if (dec[my_ip_port] > dec[recieved_election_msg.split(" ")[1]]):
                    pub_socket.send_string("%s %s" % (recieved_election_msg.split(" ")[1], "Ok"))
                    return electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)

        except zmq.error.Again as e:
            dummy = 1

        task_socket.send_string(my_ip_port)

        try :
            task_socket.recv_string()
        except zmq.error.Again as e:
            return electLeader(dec,pub_socket,sub_election_socket,sub_ok_socket,sub_leader_socket,my_ip_port,okay_time)


            
        
