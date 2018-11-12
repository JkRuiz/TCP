import os
import json


def loadData():
    with open('configTCP.json', 'r') as f:
        clients = json.load(f)
    return clients


def copy_to_client(addr):
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm -rf TCP"')
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm R_*"')
    os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "git clone https://github.com/JkRuiz/TCP.git"')


def copy_to_server(addr):
    os.system('sshpass -p "' + clients['suPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['serverUsername'] + '@' + addr + ' "rm -rf TCP"')
    os.system('sshpass -p "' + clients['suPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['serverUsername'] + '@' + addr + ' "git clone https://github.com/JkRuiz/TCP.git"')


clients = loadData()
clientIPs = clients['clientIPs']
copy_to_server(clients['serverIp'])
for ip in clientIPs:
    copy_to_client(ip)

'''
os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm -rf TCP"')
os.system('sshpass -p "' + clients['clientPassword'] + '" ssh -o StrictHostKeyChecking=no ' + clients['clientUsername'] + '@' + addr + ' "rm R_*"')
'''
