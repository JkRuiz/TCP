import os
import paramiko
import json
import time


def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties


def setupServer(ssh):
    # sudo iptraf -s eth0
    stdin, stdout, stderr = ssh.exec_command('sudo iptraf -s eth0')
    stdin.write(properties['suPassword'] + '\n')
    stdin.flush()
    time.sleep(1)
    print(stdout.read())
    stdin.flush()
    stdin.write('/home/s2g4/test_traffic.log\n')
    stdin.flush()


def shellSetup(ssh):
    chan = ssh.invoke_shell()

    run_cmd(chan, ['su', properties['suPassword']])
    run_cmd(chan, 'iptraf -s eth0')
    run_cmd(chan, chr(127) * 999)
    run_cmd()

    emptyChannel(chan)


def run_cmd(chan, cmd):
    stdin = chan.makefile('wb')

    for x in cmd:
        stdin.write(x + '\n')
    stdin.flush()
    # emptyChannel(chan)


def emptyChannel(chan):
    while not chan.recv_ready():
        i = 0
    while True:
        try:
            print(chan.recv(4096).decode())
        except:
            print('broke down')
            break


def waitChannel(chan):
    while not chan.recv_ready():
        i = 0


properties = getProperties()
serverSSH = paramiko.SSHClient()
serverSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Logging in..')
serverSSH.connect(properties['serverIp'], username=properties['serverUsername'], password=properties['serverPassword'])
print('Login - OK')
shellSetup(serverSSH)
serverSSH.close()
print('DONE')
