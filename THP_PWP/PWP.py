# -*- coding:iso-8859-1 -*-

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

    def run(self):
        # when get full list, get out this wihle
        while not self.complete:
            sleep(1)        # whait one second