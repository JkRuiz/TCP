import os
import json
import time
from threading import Thread


def run_server():
    p = getProperties()
    serverIp = p['serverIp']
    os.system('sshpass -p "1-zhK75Lr@g" ssh -o StrictHostKeyChecking=no pruebas@' + str(serverIp) + ' "python3 TCP/tcpClient.py"')


def run_cmd(chan, cmd):
    stdin = chan.makefile('wb')
    stdin.write(cmd + '\n')
    stdin.flush()


def run_client(ip):
    try:
        os.system('sshpass -p "Un14nd3s-+" ssh -o StrictHostKeyChecking=no prueba@' + str(ip) + ' "rm R_*"')
        os.system('sshpass -p "Un14nd3s-+" ssh -o StrictHostKeyChecking=no prueba@' + str(ip) + ' "rm TCP/*.log"')
    except:
        print("Failed to remove at " + str(ip))
    os.system('sshpass -p "Un14nd3s-+" ssh -o StrictHostKeyChecking=no prueba@' + str(ip) + ' "python3 TCP/tcpClient.py"')


def getProperties():
    with open('configTCP.json', 'r') as file:
        properties = json.load(file)
    return properties


def killIptraf():
    os.system("kill $(ps aux | grep 'iptraf' | awk '{print $2}')")


def logStartNetstat(n):
    os.system("netstat -s | grep segments >> Logs/Netstat_C" + str(n) + "_Start.log")


def logEndNetstat(n):
    os.system("netstat -s | grep segments >> Logs/Netstat_C" + str(n) + "_End.log")


def startIptraf(n):
    os.system("sudo iptraf -i eth0 -L /home/s2g4/TCP/Logs/TCP_C" + str(n) + "_traffic.log -B")


def makeDirFile():
    os.system('rm -rf Logs')
    os.system('mkdir Logs')


def runTest():
    properties = getProperties()
    numberClients = int(properties['numberClients'])
    # startIptraf(numberClients)
    time.sleep(1)
    serverThread = Thread(target=run_server)
    listOfIPs = properties['clientIPs']
    serverThread.start()
    time.sleep(1)
    for i in range(numberClients):
        t = Thread(target=run_client, args=[listOfIPs[i]])
        t.start()
    serverThread.join()
    # killIptraf()


def swapProperties(n):
    with open('configTCP.json', 'r') as file:
        tmp = json.load(file)
        tmp['numberClients'] = int(n)
    with open('configTCP.json', 'w') as file:
        file.write(json.dumps(tmp))


p = getProperties()
nClients = p['nClients']
makeDirFile()
for i in nClients:
    # logStartNetstat(i)
    print('Running client #', str(i))
    swapProperties(i)
    runTest()
    # logEndNetstat(i)
    time.sleep(10)
