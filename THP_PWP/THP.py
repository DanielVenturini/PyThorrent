# -*- coding:ISO-8859-1 -*-

from THP_PWP.UDP import UDPConnection
from THP_PWP.TCP import TCPConnection
from THP_PWP import CommonDef
from threading import Thread

class THP(Thread):

    def __init__(self, dict, rawinfo, defsInterface, torrentName=''):
        Thread.__init__(self)

        self.init(dict, rawinfo, torrentName, defsInterface)

    def init(self, dict, rawinfo, torrentName, defsInterface):
        # if the PyTorrent is on in half download
        # then dict is None
        if(not dict or not rawinfo):
            self.torrentName = torrentName
            return

        self.listPeers = []
        self.dict = dict
        self.rawinfo = rawinfo
        self.defsInterface = defsInterface
        self.announce = self.dict['announce']
        self.torrentName = self.dict['info']['name']
        self.lenTorrent = CommonDef.getFullLefFile(self.dict)

    def run(self):
        self.peer_id = CommonDef.getPeerId()
        self.portTCP = CommonDef.getPort('TCP')
        self.portUDP = CommonDef.getPort('UDP')
        self.num_want = 5

        self.connectAndGetPeerList()

    def connectAndGetPeerList(self):
        listPeers = []
        complete = None
        print(self.torrentName)
        UDPConnection(self.torrentName, self.peer_id, self.portUDP, self.dict['announce-list'], self.num_want, self.rawinfo, self.lenTorrent, self.defsInterface, self.listPeers).start()
        #TCPConnection(self.torrentName, self.peer_id, self.portTCP, self.dict['announce-list'], self.num_want, self.rawinfo, self.lenTorrent, self.defsInterface, self.listPeers).start()