import os
import json


def loadData():
    with open('configTCP.json', 'r') as f:
        clients = json.load(f)
    return clients


def copy_to_client(addr):
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm -rf RedesLab4"')
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm R_*"')
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "git clone https://github.com/JkRuiz/TCP.git"')


clients = loadData()
clientIPs = clients['clientIPs']
for ip in clientIPs:
    copy_to_client(ip)
