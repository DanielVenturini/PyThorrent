# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
from random import randint
import network
import socket
import struct

class UDPConnection(Thread):

    def __init__(self, torrentName, peer_id, port, announceList, num_want, rawinfo, lenTorrent, defsInterface, listPeers):
        Thread.__init__(self)

        self.peers = []
        self.port = port
        self.peer_id = peer_id
        self.rawinfo = rawinfo
        self.num_want = num_want
        self.listPeers = listPeers
        self.lenTorrent = lenTorrent
        self.torrentName = torrentName
        self.announceList = announceList
        self.defsInterface = defsInterface

    def run(self):
        # try announces backup
        for announce in self.announceList:
            announce = announce[0]

            if (announce.startswith('udp://')):
                address, port = CommonDef.getAddressTracker(announce)
                tryList = self.connectUDP(address, port)
            else:
                continue


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
        s.bind((network.getIP_BC()[0], self.port))
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

        if(len(resp) <= 26):
            return False, None

        action, new_transaction_id, interval, ieechers, seeders = struct.unpack('!lllll', resp[:20])
        if(action != 1 or new_transaction_id != transaction_id):
            return False, None

        seeders = self.getSeeders(seeders)
        print("Recebido: ", action, " ", interval, " ", ieechers, " ", seeders)
        self.defsInterface.updatePeer(self.torrentName, seeders)
        self.recList(resp[20:], seeders)

        return True, resp


    def getPacket1UDP(self, connection_id, transaction_id, event):
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)
        return struct.pack('!qll20s20sQQQIIIiH', connection_id, 1, transaction_id, CommonDef.getSHA1(self.rawinfo, hex=False), self.peer_id.encode(), uploaded, downloaded, left, event, 0, 0, self.num_want, int(self.port))


    def recList(self, data, seeders):

        CommonDef.getFullListPeers(data, seeders, self.listPeers)
        for addr in self.listPeers:
            print(addr)

    def getSeeders(self, seeders):
        if(self.num_want == -1):
            return seeders
        elif(self.num_want > seeders):
            return seeders
        else:
            return self.num_want