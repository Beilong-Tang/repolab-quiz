# echo-server.py

import socket, sys, os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

first_command = ['week1','week2','week3','week4','week5','week6','week7']

def update():
    for i in first_command:
        cmd = 'python3 shell.py %s' % i
        print('Update %s' % i)
        os.system(cmd)
        pass
    pass
    
# use 'telnet hostname PORT' to connect  
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
while True:
    try : 
        s.bind((HOST, PORT))
        print('connected on port %s' % PORT)
        
        break
    except Exception as e:
        PORT = PORT - 1 
        print(e)
        pass
    pass
while True:
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            
            #----------------------------------
            # replace this with the update code
            #----------------------------------
            update()
            if not data:
                break
            print(data)
            conn.sendall(b'repolab-quiz server: DB updated\n')
            break
        pass
    conn.close()
    
    pass

