import zmq

def setConnection(dec,my_ip_port,okay_time):
    context = zmq.Context()
    push_socket = context.socket(zmq.PUSH)
    
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://%s"%my_ip_port)
    pull_socket.setsockopt(zmq.RCVTIMEO,0)
            
    return push_socket,pull_socket