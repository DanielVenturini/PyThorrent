# -*- conding:ISO-8859-1 -*-

from random import randint
import hashlib
import struct
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
        os.makedirs('configures/')

    file = open('configures/'+fileName, 'w+')
    for line in lines:
        file.write(line + '\n')

    file.close()

# get the port which the client is hear for new connections
# the protocol refer to line in the configure.pt
def getPort(protocol):

    try:
        # read the firsts 4 bytes from second line
        # because the first line is the peer id
        if(protocol.__eq__('TCP')):
            line = 1
        elif(protocol.__eq__('UDP')):
            line = 2
        else:   #pwp
            line = 3

        port = openAndRead(fileName='configures/configure.pt', line=line, at=5)
        if(port.__eq__('')):
            raise FileNotFoundError
        else:
            return int(port)

    except FileNotFoundError:
        # create file 'configure.pt'
        # and add in first line the peer id
        # and second line the port
        port = list()
        port.append(createPeerId() + '# this line is the peer id')
        port.append(str(randint(10000, 32767)) + ' # this line is the TCP port')
        port.append(str(randint(10000, 32767)) + '               # this line is the UDP port')
        port.append(str(randint(10000, 32767)) + '               # this line is the PWP port')

        createAndInsertLines('configure.pt', port)
        return getPort(protocol)


# this def get the attr of bytes transfered
def getProperties(torrentName, totalBytes):
    torrentName += '.pt'

    try:
        uploaded = openAndRead(fileName='configures/' + torrentName, line=0, at=-1)
        downloaded = openAndRead(fileName='configures/' + torrentName, line=1, at=-1)
        left = openAndRead(fileName='configures/' + torrentName, line=2, at=-1)

        return int(uploaded), int(downloaded), int(left)
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

def setTracker(fileName, address):
    # is a file which has a list of tracker that response
    fileName += '.tr'

    try:
        file = open('configures/'+fileName, 'a')
        file.write(address + '\n')
        file.close()
    except FileNotFoundError:
        lines = []
        lines.append(address)
        createAndInsertLines(fileName, lines)

def getAddressTracker(announce):
    protocol = announce.startswith('udp://')
    ip = ''
    port = 80   # if announce dosn't port, the default are 80
    start = 0   # pos to start address in the string announce

    # is udp, then the address starst in the pos 6
    if(protocol):
        start = 6
    else:
        start = 7

    # if dosnt have a ':', then default port is 80
    if(announce.find(':', start) == -1):
        # then separe in the '/'
        indexSepare = announce.rindex('/')
    else:
        if(announce.find('/', start) == -1):
            ultimoIndex = announce.__len__()
        else:
            ultimoIndex = announce.rindex('/')

        indexSepare = announce.rindex(':')
        port = announce[indexSepare+1:ultimoIndex]

    ip = announce[start:indexSepare]

    return ip, int(port)

def getFullIP(data):
    return str(data[0])+'.'+str(data[1])+'.'+str(data[2])+'.'+str(data[3])

def getFullListPeers(data, qtdPeers, list):
    try:

        for i in range(0, qtdPeers):
            ip = getFullIP(struct.unpack('BBBB', data[i*6 : ((i * 6) + 4)]))
            port = struct.unpack('!h', data[((i*6)+4) : ((i*6)+4)+2])[0]

            if (port < 0):
                port *= -1

            list.append(ip + ':' + str(port))

    except Exception as ex:
        print("Error " + str(ex))

# if the configure file not exists, or has a invalid data
# create new file and insert the values
def checkConfigure_pt():
    try:
        for line in range(0, 4):
            if(openAndRead(fileName='configures/configure.pt', line=line, at=5).__eq__('')):
                raise Exception

    except:
        port = list()
        port.append(createPeerId() + ' # this line is the peer id')
        port.append(str(randint(10000, 32767)) + '               # this line is the TCP port')
        port.append(str(randint(10000, 32767)) + '               # this line is the UDP port')
        port.append(str(randint(10000, 32767)) + '               # this line is the PWP port')

        createAndInsertLines('configure.pt', port)