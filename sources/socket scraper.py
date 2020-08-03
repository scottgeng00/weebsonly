import json
import socket
import urllib.request
import numpy as np
from time import sleep
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

#to be added: remove server if it doesnt respond too many times


#edit these values as desired

PASSWORD = None                                
SECRET_KEY = None
IV = None

backend = default_backend()                                                                                 #Client side AES encryption to send encrypted password
cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV), backend=backend)
encryptor = cipher.encryptor()
encrypted_pass = encryptor.update(PASSWORD.encode('utf-8')) + encryptor.finalize()


SERVER_LIST = [('127.0.0.1', 25565)]

url = r'http://icanhazip.com/'

def proxy_get(server, url, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    s.sendall(password)

    status = s.recv(32)
    if not status:
        print("Initial OK from server not recieved")
        
    s.sendall(url.encode('utf-8'))

    fragments = []
    while True: 
        chunk = s.recv(256000)
        if not chunk: 
            break
        fragments.append(chunk)
    arr = b''.join(fragments)
    return arr.decode('utf-8')
    

def stop_server(server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    s.sendall(b'WHY ARE YOU RUNNING?')

def stop_all():
    for server in SERVER_LIST:
        stop_server(server)

print('Initialization OK')

##################################################################################################################

startTime = datetime.now()

userList = np.loadtxt('../output/user lists/test.csv', delimiter=',', dtype=str)

STATUS = 2                    #anime list status codes: 1=watching, 2=done, 3=hold, 4=dropped, 6=plan, 7=all

count = 0

finalOutput = []

for line in userList:
    for username in line:
        print(username)
        userDict = dict()
        userDict['user_name'] = username
        userList = []
        offset = 0
        hasNext = True


        while hasNext:

            server_number = count % len(SERVER_LIST)
            url = 'https://myanimelist.net/animelist/' + username + '/load.json?offset=' + str(offset) + '&status=' + str(STATUS)
            url = 'asdfasdf'
            
            rawData = None
            tries = 0
            while rawData is None:
                try:
                    print('Attempting to fetch \'' + url + '\' through ' + SERVER_LIST[server_number][0])
                    response = proxy_get(SERVER_LIST[server_number], url, encrypted_pass) 
                    rawData = json.loads(response)                                                                          #the way the server code is written, a bad url will always give an invalid json string, resulting in an exception here as well
                except:
                    if tries > 5*len(SERVER_LIST):
                        print('FATAL ERROR: NO SERVERS RESPONDING!')
                        with open('data.json', 'w') as f:                   #flush what we have already to disk and quit
                            json.dump(finalOutput, f) 
                        exit()
                    count += 1
                    tries += 1
                    server_number = count % len(SERVER_LIST)

            if len(rawData) < 300:
                hasNext = False

            filteredData = []
            for raw in rawData:
                entry = dict()
                entry['id'] = raw['anime_id']
                entry['score'] = raw['score']
                #entry['media_type'] = raw['anime_media_type_string']
                #entry['mpaa_rating'] = raw['anime_mpaa_rating_string']
                #entry['user_priority'] = raw['priority_string']
                filteredData.append(entry)

            userList += filteredData
            offset += 300
            count += 1
            sleep(2)

        print("\n")
        userDict['user_list'] = userList
        finalOutput.append(userDict)

with open('data.json', 'w') as f:
    json.dump(finalOutput, f)

print(datetime.now()-startTime)
        
        










