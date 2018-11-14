import json
import time
import socket
import hashlib
import sys
# import request as rq


def msgSend(msg, sock):
    size = len(msg)
    if len(str(size)) <= 4:
        #gprint('SIZE MODIFIED')
        first = str('0' * (4 - len(str(size))))
        finalSize = str(first) + str(size)
    #print('EL SIZE ES : ', finalSize.encode())
    #print('EL MENSAJE ES : ', str(msg).encode())
    sock.sendall(finalSize.encode())
    sock.sendall(str(msg).encode())


def msgReceive(sock):
    size = recvall(sock, 4).decode()
    if size == '':
        return ''
    data = recvall(sock, int(size)).decode()
    return data


def btsReceive(sock):
    size = recvall(sock, 4).decode()
    if size == '':
        return ''
    data = recvall(sock, int(size))
    return data


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if packet:
            data += packet
    return data


def getProperties():
    with open('configTCP.json', 'r') as file:
        properties = json.load(file)
    return properties


def sout(s):
    print(s)
    log.write(s + '\n')
    log.flush()


with open('clientTCPOut.log', 'w') as log:
    # Envia el numero de bytes recibidos antes de recibir el archivo
    # rq.send_metric()
    # load properties form json file
    properties = getProperties()
    host = str(properties['serverIp'])
    port = int(properties['serverPort'])
    chunkSize = int(properties['chunkSize'])

    # start socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Extended timeout to avoid broken pipes
    # s.settimeout(999999999)

    # define some constants for the file transfer protocol
    statusOk = 'STATUS_OK'
    fileOk = 'FILE_OK'
    fileError = 'FILE_ERROR'
    endFile = 'END_OF_FILE'
    sout('done with defining variables')

    while(True):
        try:
            # connect to server
            s.connect((host, port))
            break
        except:
            sout('waiting for server...')
            time.sleep(5)

    # tell server client is ready to receive
    msgSend(statusOk, s)

    # receive filename of file to be transfered
    fileName = msgReceive(s)

    # create hasher to check integrity later on
    hasher = hashlib.md5()

    with open("R_" + fileName, 'wb') as f:
        i = 0
        while True:
            i += 1
            if i % 10000 == 0:
                sout('receiving data...')
            data = btsReceive(s)
            #print('DATO : ', data)
            try:
                final = data.decode().split(' ')
                if final[0].strip() == endFile:
                    hasheado = final[1]
                    break
                if data == '':
                    break
            except:
                pass
            hasher.update(data)
            # write data to a file
            f.write(data)
    f.close()

    hasheado2 = hasher.hexdigest()
    if (hasheado.strip() == hasheado2.strip()):
        msgSend(fileOk, s)
    else:
        msgSend(fileError, s)
    s.close()
    # Envia el numero de bytes recibidos despues de recibir el archivo
    # rq.send_metric()
    sout('connection closed')
