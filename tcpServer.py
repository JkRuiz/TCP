import socket
import time
import hashlib
import datetime
import json
import time
from threading import Thread


def msgSend(msg, sock):
    size = len(msg)
    if len(str(size)) <= 4:
        first = str('0' * (4 - len(str(size))))
        finalSize = str(first) + str(size)
    sock.sendall(finalSize.encode())
    sock.sendall(str(msg).encode())


def sendBytes(bts, sock):
    size = len(bts)
    if len(str(size)) <= 4:
        first = str('0' * (4 - len(str(size))))
        finalSize = str(first) + str(size)
    sock.sendall(finalSize.encode())
    sock.sendall(bts)


def msgReceive(sock):
    size = recvall(sock, 4).decode()
    if size == '':
        return ''
    data = recvall(sock, int(size)).decode()
    return data


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def threaded_function(conn, addr, id):
    # conn.settimeout(999999999)

    start = datetime.datetime.now()
    sout("C" + str(id) + ": Connection started at " + str(start))
    data = msgReceive(conn)
    sout("C" + str(id) + ": " + data)

    rsp = "Sending " + fileName
    sout("S: " + rsp + " to C" + str(id) + " with IP " + addr[0] + " and port " + str(addr[1]))
    msgSend(rsp, conn)

    for l in fileChunks:
        sendBytes(l, conn)

    sout("S: END_OF_FILE")
    msgSend(('END_OF_FILE ' + hasheado), conn)
    sout("S: MD5Hash " + hasheado)

    asw = msgReceive(conn)
    sout("C" + str(id) + ": " + asw)
    summary = str(datetime.datetime.now() - start) + "s"
    sout("C" + str(id) + ": Transfered in " + summary)
    conn.close()


def getProperties():
    with open('configTCP.json', 'r') as file:
        properties = json.load(file)
    return properties


def sout(l):
    log.write(l + '\n')
    log.flush()
    print(l)


properties = getProperties()
fileName = properties['fileName']
numberClients = int(properties['numberClients'])
port = int(properties['serverPort'])
chunkSize = int(properties['chunkSize'])
#logPrefix = properties['logPrefix'] + str(numberClients) + "_Server.log"
logPrefix = 'test.log'

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind(('', port))  # Bind to the port
serverSocket.listen(numberClients)  # Now wait for client connection.

fileChunks = []
with open(fileName, 'rb') as f:
    l = f.read(chunkSize)
    while (l):
        fileChunks.append(l)
        l = f.read(chunkSize)

hasher = hashlib.md5()
with open(fileName, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
hasheado = hasher.hexdigest()


with open((logPrefix), 'w') as log:
    sout('Server listening....')
    tStart = datetime.datetime.now()

    threads = []
    for j in range(numberClients):
        conn, addr = serverSocket.accept()
        sout('Server adopted connection #' + str(j + 1))
        thread = Thread(target=threaded_function, args=(conn, addr, j + 1))
        thread.start()
        threads.append(thread)

    for i in range(len(threads)):
        threads[i].join()

    summary = str(datetime.datetime.now() - tStart) + "s"
    sout("S: Transfered in " + summary)
