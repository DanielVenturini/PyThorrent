# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
import hashlib

class THP(Thread):

    def __init__(self, dict):
        self.dict = dict
        self.torrentName = self.dict['info']['name']
        self.lenTorrent = CommonDef.getFullLefFile(self.dict)

    def run(self):
        info_hash = self.getSHA1()
        peer_id = CommonDef.getPeerId()
        port = CommonDef.getPort()
        # thre values of file to download

        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)

    def getSHA1(self):
        sha = hashlib.sha1()
        sha.update(self.dict['info'].__str__().encode())
        return sha.hexdigest()