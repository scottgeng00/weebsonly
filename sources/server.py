import socket
import urllib.request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from fake_useragent import UserAgent

HOST = '127.0.0.1'
PORT = 25565

WHITELISTED_IPS = ['127.0.0.1']                                    #vulnerable to ip spoofing, but this adds an additonal layer of security


PASSWORD = None                                
SECRET_KEY = None
IV = None
backend = default_backend()                                                                                 #aes cipher to decode recieved password
cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV), backend=backend)

ua = UserAgent()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
    print('\nConnected by', addr)

    raw_msg = conn.recv(32)      
    decryptor = cipher.decryptor()
    try:
        recv_pass = decryptor.update(raw_msg) + decryptor.finalize()
    except:
        print('Bad password or stop signal received. Stopping server...')
        break
    if not recv_pass or not recv_pass.decode('utf-8') == PASSWORD or addr[0] not in WHITELISTED_IPS:              #basic password and ip check to prevent unwanted clients
        print(recv_pass)
        print('BAD CONNECTION! SHUTTING DOWN...')
        conn.close()
        break

    conn.sendall(b'OK')
    data = conn.recv(256000)

    url = data.decode('utf-8')
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', ua.random)
        response = urllib.request.urlopen(req)
        print("Sent " + str(response) + " to client")
        conn.sendall(response.read())
    except:
        conn.sendall(b'404 no external response')              #this line must be a bad json
        print("Bad url: " + url)
            
    conn.close()  



        
        