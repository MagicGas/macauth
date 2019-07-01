

import paramiko
from macauth.models import MacAddr
import threading
def mac_compare(oldmaclist,newmaclist):
    addlist = set(newmaclist).difference(oldmaclist)
    rmlist = set(oldmaclist).difference(newmaclist)
    return list(addlist),list(rmlist)


def addmac(position,maclist):
    try:
        for mac in maclist:
            print(position,mac,type(position),type(mac))
            MacAddr.objects.create(position=position,macaddr=mac)
        if maclist:
            if device_op(position,maclist,[]):
                return True
            else:
                return False
        else:
            return True

    except :
        return False


def rmmac(position,maclist):
    try:

        for mac in maclist:
            MacAddr.objects.filter(position=position,macaddr=mac).delete()
        if maclist:
            if device_op(position,[],maclist):
                return True
            else:
                return False
        else:
            return True
    except :
        return False

def addmacOP(addmaclist,run_cmd,ssh):
    res = ''
    res += run_cmd('system-view\n', ']')
    res += run_cmd('acl name mac_auth 4000\n', ']')
    for mac in addmaclist:
        mac_command = 'rule  permit source-mac ' + mac + '\n'
        t2 = threading.Thread(target=run_cmd, args=(mac_command, ']',))
        t2.start()
    res += run_cmd("quit\n", ']')
    res += run_cmd("quit\n", '>')
    res += run_cmd("save\n", ']')
    res += run_cmd('Y\n', '>')
    if "Error: The rule already exists." in res:
        ssh.close()
    if 'Error' in res:
        ssh.close()
        return False
    else:
        ssh.close()

def rmmacOP(rmmaclist,run_cmd,ssh):
    res = ''
    res += run_cmd('system-view\n', ']')
    res += run_cmd('acl name mac_auth 4000\n', ']')
    for mac in rmmaclist:
        mac_command = 'undo rule  permit source-mac ' + mac + '\n'
        t3 = threading.Thread(target=run_cmd, args=(mac_command, ']',))
        t3.start()
    res += run_cmd("quit\n", ']')
    res += run_cmd("quit\n", '>')
    res += run_cmd("save\n", ']')
    res += run_cmd('Y\n', '>')

    if 'Error' in res:
        ssh.close()
        return False
    else:
        ssh.close()
        global result
        result = True

def macOP(hostname,addmaclist,rmmaclist):
    print(hostname)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username='paxjk',
                password='paxjk123456')
    client = ssh.invoke_shell()

    def run_cmd(cmd, endswith):
        buff = ''
        client.send(cmd)
        while not buff.endswith(endswith):
            resp = str(client.recv(1024), 'utf-8')
            buff += resp
        return buff

    if addmaclist:
        addmacOP(addmaclist,run_cmd,ssh)
    if rmmaclist:
        rmmacOP(rmmaclist,run_cmd,ssh)
    ssh.close()

def positionOP(position):
    hostnames = []

    if position == "shanghai":
        hostnames = ["172.19.192.2", "172.19.192.3"]
    if position == "shenzhen":
        hostnames = ["172.19.24.201", "172.19.24.202"]
    if position == "beijing":
        hostnames = ["172.19.32.201", "172.19.32.202"]
    if position == "chengdu":
        hostnames = ["172.19.36.201", "172.19.36.202"]
    return  hostnames


def device_op(position,addmaclist,rmmaclist):
    try:
        if (addmaclist or rmmaclist):
            result = True
            hostnames = positionOP(position)
            for hostname in hostnames:
                t1 = threading.Thread(target=macOP, args=(hostname,addmaclist,rmmaclist,))
                t1.start()
            return  result

        else:
            return True
    except:
        return False
