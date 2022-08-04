# echo-server.py

import socket, sys, os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST=''
PORT = 8070  # Port to listen on (non-privileged ports are > 1023)

first_command = ['week1','week2','week3','week4','week5','week6','week7']


def update():
    cmd = 'python3 upload_quiz.py'
    os.system(cmd)
    pass

if __name__ == '__main__':    
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
    pass

