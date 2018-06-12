# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
import hashlib

class THP(Thread):

    def __init__(self, dict):
        self.dict = dict

    def run(self):
        info_hash = self.getSHA1()
        peer_id = CommonDef.getPeerId()
        port = CommonDef.getPort()
        pass

    def getSHA1(self):
        sha = hashlib.sha1()
        sha.update(self.dict['info'].__str__().encode())
        return sha.hexdigest()