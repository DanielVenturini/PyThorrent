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
            indexSepare = announce.rindex(':')
            port = announce[indexSepare+1:announce.rindex('/')]

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
                'info_hash=38c0ca5d45932d131ab19ced0d3391439ae9a51e&' +
                'peer_id=' + self.peer_id + '&' +
                'port' + self.port + '&' +
                'uploaded=' + str(uploaded) + '&' +
                'downloaded=' + str(downloaded) + '&' +
                'left=' + str(left) +
                event +
                ' HTTP/1.1\n\r\n\r\n').encode()

    def connectAndGetPeerList(self):
        # connect with udp socket
        if(self.announce.startswith('udp://')):
            self.connectUDP()
        else:
            self.connectTCP()

    def connectUDP(self):
        s = self.createSocketUDP()
        s.sendto(self.getMessage(event='&event=started'), (self.addressTracker, self.portTracker))
        print("Jah enviou")
        s.settimeout(1)

        try:
            print("Vai comecar a receber")
            response = s.recvfrom(1024)
            print("Recebeu")
            print(response.decode())
        except Exception as error:
            print("Erro ao receber lista do tracker em UDP: " + str(error))

    def connectTCP(self):
        try:
            s = self.createSocketTCP()
            s.connect((self.addressTracker, self.portTracker))
            s.settimeout(1)

            s.send(self.getMessage(event='&event=started'))
            response = s.recv(1024)
            print(response.decode())
        except Exception as error:
            print("Erro ao receber lista do tracker em TCP: " + str(error))

    def createSocketUDP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def createSocketTCP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)