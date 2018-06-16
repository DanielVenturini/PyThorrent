# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
import hashlib
import socket

class THP(Thread):

    def __init__(self, dict):
        super(THP, self).__init__()

        self.dict = dict
        self.announce = self.dict['announce']
        self.torrentName = self.dict['info']['name']
        self.lenTorrent = CommonDef.getFullLefFile(self.dict)

        self.addressTracker, self.portTracker = self.getAddressTracker(self.announce)

        print("Foi recuperado os seguintes valores:")
        print("announce: " + self.announce)
        print("torrent name: " + self.torrentName)
        print("size of torrent: " + str(self.lenTorrent))
        print("address: " + self.addressTracker)
        print("port: " + str(self.portTracker))

    def getAddressTracker(self, announce):
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

    def run(self):
        self.info_hash = self.getSHA1()
        self.peer_id = CommonDef.getPeerId()
        self.port = CommonDef.getPort()

        print("Valores dinamicos: ")
        print("info_hash: " + self.info_hash)
        print("peer_id: " + self.peer_id)
        print("port: " + str(self.port))
        self.connectAndGetPeerList()

    def getSHA1(self):
        sha = hashlib.sha1()
        sha.update(self.dict['info'].__str__().encode())
        return sha.hexdigest()

    # which event send to server, if none, ''
    def getMessage(self, event=''):
        # ever when get the messagem, get this properties
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)

        # GET /announce?key=value&key=value ... HTTP/1.1 \r\n\r\n
        return ('GET /announce?' +
                #'info_hash=' + str(self.info_hash) + '&' +
                'info_hash=c68577760d821c9b3101fb113207307042adac6f&' +
                'peer_id=' + self.peer_id + '&' +
                'port' + self.port + '&' +
                'uploaded=' + str(uploaded) + '&' +
                'downloaded=' + str(downloaded) + '&' +
                'left=' + str(left) +
                event +
                ' HTTP/1.1\n\r\n\r\n').encode()

    def connectAndGetPeerList(self):
        # connect with udp socket
        tryList = False
        message = self.getMessage(event='&event=started')
        if(self.announce.startswith('udp://')):
            tryList = self.connectUDP(self.addressTracker, self.portTracker, message)
        else:
            tryList = self.connectTCP(self.addressTracker, self.portTracker, message)

        if(tryList != False):
            return

        print("Agora para a lista: ", self.dict['announce-list'])
        # try announces backup
        for announce in self.dict['announce-list']:
            announce = announce[0]
            address, port = self.getAddressTracker(announce)

            if (announce.startswith('udp://')):
                tryList = self.connectUDP(address, port, message)
            else:
                tryList = self.connectTCP(address, port, message)

    def connectUDP(self, addressTracker, portTracker, message):
        try:
            print("Conectando TCP:" + addressTracker + ":" + str(portTracker))
            s = self.createSocketUDP()
            s.sendto(message, (addressTracker, portTracker))
            s.settimeout(0.5)

            response = s.recvfrom(1024)
            print(response.decode())
        except Exception as error:
            print("Erro ao receber lista do tracker em UDP: " + str(error))
            return False

    def connectTCP(self, addressTracker, portTracker, message):
        try:
            print("Conectando TCP:" + addressTracker +":" + str(portTracker))
            s = self.createSocketTCP()
            s.settimeout(0.5)
            s.connect((addressTracker, portTracker))
            s.send(message)
            response = s.recv(1024)
            print(response.decode())
            return response

        except Exception as error:
            print("Erro ao receber lista do tracker em TCP: " + str(error))
            return False

    def createSocketUDP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def createSocketTCP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)