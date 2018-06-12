# -*- conding:ISO-8859-1 -*-

from random import randint
import os

def createPeerId():
    peerId = '-PT1012-'

    for i in range(0, 12):
        peerId += str(randint(0, 9))

    return peerId

def getPeerId():
    try:
        peerId = openAndRead('../configures/configure.pt', 0, 20)
        if(peerId.startswith('-PT')):
            return peerId
        else:
            lines = list()
            lines.append(createPeerId())
            createAndInsertLines('configure.pt', lines)
            return getPeerId()

    except FileNotFoundError:
        lines = list()
        lines.append(createPeerId())
        createAndInsertLines('configure.pt', lines)
        return getPeerId()

# fileName is the file to read; line is the line to start read
# len is the total bytes to read from specify line
# if len is -1, return full line; if line is -1, read full file
def openAndRead(fileName='', line=0, at=0):
    file = open(fileName)

    try:
        if(line == -1):
            return file.readlines()

        # jump to line specify
        for i in range(0, line):
            file.readline()

        if(at == -1):
            return file.readline().replace('\n', '')
        else:
            return file.read(at)
    finally:
        file.close()

# if the file configures/'fileName' not exists
# create it and insert all lines
def createAndInsertLines(fileName, lines):
    if not os.path.exists('../configures/'):
        os.makedirs('../configures/')

    file = open('../configures/'+fileName, 'w+')
    for line in lines:
        file.write(line + '\n')

    file.close()

# get the port which the client is hear for new connections
def getPort(fileName):
    try:
        # read the firsts 4 bytes from first line
        port = openAndRead('../configures/'+fileName, line=0, at=5)
        if(port.__eq__('')):
            raise FileNotFoundError
        else:
            return port

    except FileNotFoundError:
        port = list()
        port.append(str(randint(10000, 65535)))

        createAndInsertLines(fileName, port)
        return getPort(fileName)


