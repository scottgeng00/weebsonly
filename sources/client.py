import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

HOST = '127.0.0.1'
PORT = 25565

PASSWORD = None                                
SECRET_KEY = None
IV = None

backend = default_backend()                                                                                 #Client side AES encryption to send encrypted password
cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV), backend=backend)
encryptor = cipher.encryptor()
encrypted_pass = encryptor.update(PASSWORD.encode('utf-8')) + encryptor.finalize()

url = r'https://myanimelist.net/animelist/scottgeng00/load.json'
url = r'http://icanhazip.com/'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

s.sendall(encrypted_pass)
status = s.recv(32)
print(status)
if not status:
    print("Initial OK from server not recieved")
    
s.sendall(url.encode('utf-8'))

fragments = []
while True: 
    chunk = s.recv(256000)
    if not chunk: 
        print('done')
        break
    fragments.append(chunk)
arr = b''.join(fragments)

print("\n")
print(arr)

