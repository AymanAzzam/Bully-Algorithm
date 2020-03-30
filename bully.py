import sys
import zmq
import time
from zmq import EAGAIN

def clearSocketBuffer(pull_socket):
    print("I'm clearing my pull socket buffer \n")
    time.sleep(1)  #Wait till the pull_socket receive the old data
    while(True):
        try: 
            recieved_message = pull_socket.recv_string()
            print("I cleared %s message is sent by %s \n"%(recieved_message.split(" ")[0],recieved_message.split(" ")[1]))
        except  zmq.error.Again as e:
            print("************************************************ \n")
            return

def leaderCheckElection(dec,push_socket,pull_socket,my_ip_port):
    try:
        recieved_message = pull_socket.recv_string()
        if(recieved_message.split(" ")[0] == "Election"):
            if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                push_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                push_socket.send_string("%s %s" %("Leader",my_ip_port))
                push_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                print("I sent Leader message to %s \n"%recieved_message.split(" ")[1])
                print("************************************************ \n")
                print("%s I'm the leader and I'm doing my task \n"%my_ip_port)
            #else:       #this Case shouldn't happen
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("I received Leader message from %s \n"%recieved_message.split(" ")[1])
            if(dec[my_ip_port] < dec[recieved_message.split(" ")[1]]):
                print("Its priority is higher than my priority \n")
                print("************************************************ \n")
                return recieved_message.split(" ")[1]   # i received Leader message
            #else:       #this Case shouldn't happen 
    except zmq.error.Again as e:
        return 0    # i didn't receive anything
    return 1        # i didn't receive Leader message

def machineCheckElection(dec,task_socket,push_socket,push_okay_socket,pull_socket,my_ip_port,leader_ip_port):
    try: 
        recieved_message = pull_socket.recv_string()
        if(recieved_message.split(" ")[0] == "Election"):
            print("I received election message from %s \n"%recieved_message.split(" ")[1])
            try:
                task_socket.send_string("is leader alive")
                task_socket.recv_string()
            except zmq.error.Again as e:
                if(dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                    push_okay_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                    push_okay_socket.send_string("%s %s" % ("Ok",my_ip_port)) 
                    push_okay_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                    print("I sent okay message to %s \n" %(recieved_message.split(" ")[1]))
                    print("************************************************ \n")
                    # The leader changed
                    return electLeader(dec,push_socket,push_okay_socket,pull_socket,my_ip_port,okay_time)
                else:
                    print("I'm waiting till receive Leader message")
                    while(True):
                        try: 
                            recieved_message = pull_socket.recv_string()
                            if(recieved_message.split(" ")[0] == "Leader"):
                                print("I received Leader message from %s \n"%recieved_message.split(" ")[1])
                                print("************************************************ \n")
                                # The leader changed
                                return recieved_message.split(" ")[1] 
                        except  zmq.error.Again as e:
                            dummy = 1 
            print("The Leader still alive \n")
            print("************************************************ \n")
            print("%s I'm a normal machine and I'm doing my task \n"%my_ip_port)
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("I received Leader message from %s \n"%recieved_message.split(" ")[1])
            if(dec[leader_ip_port] < dec[recieved_message.split(" ")[1]]):
                print("Its priority is higher than leader priority \n")
                print("************************************************ \n")
                # The leader changed
                return recieved_message.split(" ")[1] 
    except  zmq.error.Again as e:
        dummy = 1
    return 0    #The leader didn't change

def checkPullSocket(dec,push_okay_socket,pull_socket,my_ip_port):
    try: 
        recieved_message = pull_socket.recv_string()
        if(recieved_message.split(" ")[0] == "Election"):
            print("I received election message from %s \n"%recieved_message.split(" ")[1])
            if(dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                push_okay_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                push_okay_socket.send_string("%s %s" % ("Ok",my_ip_port)) 
                push_okay_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                print("ok message sent to %s \n" %(recieved_message.split(" ")[1]))
        elif(recieved_message.split(" ")[0] == "Ok"):
            print("I received okay message from %s \n"%recieved_message.split(" ")[1])
            return 1     # i got okay message
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("I received Leader message from %s \n"%recieved_message.split(" ")[1])
            print("************************************************ \n")
            return recieved_message.split(" ")[1]   # i received Leader message
    except  zmq.error.Again as e:
        return 0        # i received Election or garbage or nothing
    return 0            # i received Election or garbage or nothing

def electLeader(dec,push_socket,push_okay_socket,pull_socket,my_ip_port, okay_time):  
    ######### (1) send election for priorities higher than me ############
    recieved_ok = False
    i = 0
    for k,v in dec.items():         
        if(v > dec[my_ip_port]):
            push_socket.connect("tcp://%s"%k)
            push_socket.send_string("%s %s" %("Election",my_ip_port))
            push_socket.disconnect("tcp://%s"%k)
            print("I sent Election message to %s \n"%k)

            ######## This Step is Implementation Optimization ##########
            ######## Checking if i recieved okay message or Leader Message ########## 
            out = checkPullSocket(dec,push_okay_socket,pull_socket,my_ip_port)
            if(out == 1):   # i received okay message
                recieved_ok = True
                break
            elif(out != 0):  # i received Leader message
                return out
        i+=1
    
    ######### (2) Waiting Okay message within the specified time ############
    milliseconds = int(round(time.time() * 1000))
    counter = 0    
    while(not recieved_ok and counter < okay_time): 
        out = checkPullSocket(dec,push_okay_socket,pull_socket,my_ip_port)
        if(out == 1):   # i received okay message
            recieved_ok = True
            break
        elif(out != 0):  # i received Leader message
            return out

        milliseconds2 = int(round(time.time() * 1000))
        counter +=  milliseconds2 - milliseconds
        milliseconds = milliseconds2   
    print("************************************************ \n")
    
    ######### (3) if i didn't get an Okay message, Send Leader message to all nodes ############
    leader = ""
    if (recieved_ok == False):
        for k,v in dec.items():
            if(k != my_ip_port):
                push_socket.connect("tcp://%s"%k)
                push_socket.send_string("%s %s" %("Leader",my_ip_port))
                push_socket.disconnect("tcp://%s"%k)
                print("I sent Leader message to %s \n"%k)
        print("************************************************ \n")
        return my_ip_port  
    ######### (4) if i got an Okay message, Wait till you get a Leader message ############
    else:
        while(True):
            try: 
                recieved_message = pull_socket.recv_string()
                if(recieved_message.split(" ")[0] == "Leader"):
                    print("I received Leader message from %s \n"%recieved_message.split(" ")[1])
                    print("************************************************ \n")
                    return recieved_message.split(" ")[1] 
            except  zmq.error.Again as e:
                dummy = 1     