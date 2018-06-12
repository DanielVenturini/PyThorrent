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
            return createAndInsertPeerId()

    except FileNotFoundError:
        return createAndInsertPeerId()

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

# if the file configures/configure.pt not exists
# create it and insert in first line the peer id
def createAndInsertPeerId():
    if not os.path.exists('../configures/'):
        os.makedirs('../configures/')

    peerId = createPeerId()

    configureFile = open('../configures/configure.pt', 'w+')
    configureFile.write(peerId)
    configureFile.close()
    return peerId