# -*- conding:ISO-8859-1 -*-

from random import randint
import hashlib
import os

def createPeerId():
    peerId = '-PT1012-'

    for i in range(0, 12):
        peerId += str(randint(0, 9))

    return peerId

def getPeerId():
    try:
        peerId = openAndRead('configures/configure.pt', 0, 20)

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
    if not os.path.exists('configures/'):
        os.makedirs('.configures/')

    file = open('configures/'+fileName, 'w+')
    for line in lines:
        file.write(line + '\n')

    file.close()

# get the port which the client is hear for new connections
def getPort():
    try:
        # read the firsts 4 bytes from second line
        # because the first line is the peer id
        port = openAndRead(fileName='configures/configure.pt', line=1, at=5)
        if(port.__eq__('')):
            raise FileNotFoundError
        else:
            return port

    except FileNotFoundError:
        # create file 'configure.pt'
        # and add in first line the peer id
        # and second line the port
        port = list()
        port.append(createPeerId())
        port.append(str(randint(10000, 65535)))

        createAndInsertLines('configure.pt', port)
        return getPort()


# this def get the attr of bytes transfered
def getProperties(torrentName, totalBytes):
    torrentName += '.pt'

    print("Tentando ler do arquivo: " + torrentName)
    try:
        uploaded = openAndRead(fileName='configures/' + torrentName, line=0, at=-1)
        downloaded = openAndRead(fileName='configures/' + torrentName, line=1, at=-1)
        left = openAndRead(fileName='configures/' + torrentName, line=2, at=-1)

        return uploaded, downloaded, left
    except FileNotFoundError:
        # if file not exists, create one file with:
        # first line is total uploaded
        # seconde line is total downloaded
        # third line is total remaining to complete download
        createAndInsertLines(torrentName, ['0', '0', str(totalBytes)])

        return 0, 0, totalBytes


# this def get the full file of torrent
def getFullLefFile(dict):
    try:
        return dict['info']['length']
    except KeyError:            # if has a error, then is multiple files
        fullSize = 0

        for file in dict['info']['files']:
            fullSize += file['length']

        return fullSize

def getSHA1(toSha1, hex=True):
    sha = hashlib.sha1()
    sha.update(toSha1)

    if(hex):
        return sha.hexdigest()
    else:
        return sha.digest()