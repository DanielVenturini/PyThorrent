# -*- coding:iso-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
from time import sleep
import socket
import struct

class PWP(Thread):

    def __init__(self, torrentName, peer_id, raw_info, lenTorrent, defsInterface, listPeers, complete):
        Thread.__init__(self)

        self.torrentName = torrentName
        self.peer_id = peer_id
        self.raw_info = raw_info
        self.defsInterface = defsInterface
        self.listPeers = listPeers
        self.complete = complete
        self.lenTorrent = lenTorrent

        self.peersReal = []

        # data to messages
        # all data must be bytes
        self.name_length = chr(19).encode()
        self.protocol_name = 'BitTorrent protocol'.encode()
        self.reserved = (8 * chr(0)).encode()
        self.info_hash = CommonDef.getSHA1(self.raw_info, hex=False)
        self.peer_id = self.peer_id.encode()

        print(self.peer_id)
        print(CommonDef.getPort('PWP'))
        print(CommonDef.getSHA1(self.raw_info, hex=False))


    def run(self):
        sleep(5)        # whait five seconds to trackers responses

        self.s = self.createSocketTCP()

        for peer in self.listPeers:             # for all peers

            sucess = self.tryHandshake(peer)    # x.w.y.x:qqqqq
            if(sucess):
                self.peersReal.append(peer)
                self.defsInterface.updatePeer(self.torrentName, 1)


    def tryHandshake(self, peer):
        addr = peer.split(':')

        ip = addr[0]
        port = addr[1]

        try:
            self.s = self.createSocketTCP()
            self.s.connect((ip, int(port)))         # try connect
            self.s.send(self.getMessageHandshake()) # send message handshake

            resp = self.s.recv(68)                  # the response must be have 68 bytes
            return self.checkResponse(resp)         # check the response
        except (socket.timeout, Exception) as ex:
            print("Erro ao tentar handshake " + peer + ": " + str(ex))
            return False


    def getMessageHandshake(self):
        return (
            self.name_length +
            self.protocol_name +
            self.reserved +
            self.info_hash +
            self.peer_id
        )


    def checkResponse(self, resp):
        # convert all binary
        print(resp)
        name_length, protocol_name, reserved, info_hash, peer_id = struct.unpack('!b19s8s20s20s', resp)

        # chech the requisits
        if(int(name_length) != len(protocol_name) or info_hash != self.info_hash):
            print("Uma conexao nao validada")
            return False

        print("Uma conexao validada")
        return True


    def createSocketTCP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        return s