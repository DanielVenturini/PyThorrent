# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
from random import randint
import socket
import struct

class UDPConnection(Thread):

    def __init__(self, torrentName, peer_id, port, announceList, num_want, rawinfo, lenTorrent, defsInterface):
        Thread.__init__(self)

        self.peers = []
        self.port = port
        self.peer_id = peer_id
        self.rawinfo = rawinfo
        self.num_want = num_want
        self.lenTorrent = lenTorrent
        self.torrentName = torrentName
        self.announceList = announceList
        self.defsInterface = defsInterface

    def start(self):
        # try announces backup
        for announce in self.announceList:
            announce = announce[0]

            if (announce.startswith('udp://')):
                address, port = self.getAddressTracker(announce)
                tryList = self.connectUDP(address, port)
            else:
                continue

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


    def connectUDP(self, addressTracker, portTracker):
        try:
            print("Conectando UDP:" + addressTracker + ":" + str(portTracker))
            s = self.createSocketUDP()

            # get the first message, the message to connect
            transaction_id, message = self.getPacket0UDP()
            s.sendto(message, (addressTracker, portTracker))

            # check the response
            sucess, connection_id = self.checkResponse0UDP(s, transaction_id)
            if(not sucess):
                raise Exception

            transaction_id = randint(0, 2147483647)     # new random transaction_id
            message = self.getPacket1UDP(connection_id, transaction_id, 2)
            s.sendto(message, (addressTracker, portTracker))

            sucess, data = self.checkResponse1UDP(s, transaction_id)
            if(not sucess):
                raise Exception

            # if this tracker has responsed, save this
            self.defsInterface.updateTracker(self.torrentName, 1)
            CommonDef.setTracker(self.torrentName, 'udp://'+addressTracker+':'+str(portTracker))
        except Exception as error:
            print("Erro ao receber em UDP: " + str(error))
            return False


    def createSocketUDP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('192.168.0.29', self.port))
        self.port = int(s.getsockname()[1])
        s.settimeout(0.5)

        return s


    # int64_t, int32_t, int32_t
    def getPacket0UDP(self):
        # ! -> network(bigend) q -> long integer 64 l -> integer 32
        # first must be 0x41727101980
        # 0 is the action to connect
        # transaction_id is less than 2147483647
        transaction_id = randint(0, 2147483647)
        return transaction_id, struct.pack('!qll', 0x41727101980, 0, transaction_id)


    def checkResponse0UDP(self, s, transaction_id):
        resp = s.recvfrom(16)[0]
        # the len must be 16
        if(len(resp) != 16):
            return False, None

        action, new_transaction_id, connection_id = struct.unpack('!llq', resp)
        if(action != 0 or new_transaction_id != transaction_id):
            return False, None

        return True, connection_id


    def checkResponse1UDP(self, s, transaction_id):
        if(self.num_want == -1):
            resp = s.recvfrom(2048)[0]
        else:
            resp = s.recvfrom(20+((20+6*self.num_want) + (24+6*self.num_want)))[0]

        print("Tamanho da resposta: ", len(resp))

        if(len(resp) <= 26):
            return False, None

        action, new_transaction_id, interval, ieechers, seeders = struct.unpack('!lllll', resp[:20])
        if(action != 1 or new_transaction_id != transaction_id):
            return False, None

        print("Recebido: ", action, " ", interval, " ", ieechers, " ", seeders)
        self.defsInterface.updatePeer(self.torrentName, seeders)
        self.recList(resp[20:], seeders)

        return True, resp


    def getPacket1UDP(self, connection_id, transaction_id, event):
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)
        return struct.pack('!qll20s20sQQQIIIiH', connection_id, 1, transaction_id, CommonDef.getSHA1(self.rawinfo, hex=False), self.peer_id.encode(), uploaded, downloaded, left, event, 0, 0, self.num_want, int(self.port))


    def recList(self, data, seeders):
        print("Dado original: ", data)

        if(self.num_want == -1):
            qtdPeers = seeders
        elif(self.num_want > seeders):
            qtdPeers = seeders
        else:
            qtdPeers = self.num_want

        try:

            for i in range(0, qtdPeers):
                ip = self.getFullIP(struct.unpack('BBBB', data[i*6:((i*6)+4)]))
                port = struct.unpack('!h', data[((i*6)+4):((i*6)+4)+2])[0]

                if(port  < 0):
                    port *= -1

                print(ip, ":", port)
                self.peers.append(ip+':'+str(port))

        except Exception as ex:
            print("Error em printar a lista: " + str(ex))


    def getFullIP(self, data):
        return str(data[0])+'.'+str(data[1])+'.'+str(data[2])+'.'+str(data[3])