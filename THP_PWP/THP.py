# -*- coding:ISO-8859-1 -*-

from THP_PWP import CommonDef
from threading import Thread
import hashlib

class THP(Thread):

    def __init__(self, dict):
        self.dict = dict
        self.announce = self.dict['announce']
        self.torrentName = self.dict['info']['name']
        self.lenTorrent = CommonDef.getFullLefFile(self.dict)

    def run(self):
        self.info_hash = self.getSHA1()
        self.peer_id = CommonDef.getPeerId()
        self.port = CommonDef.getPort()

    def getSHA1(self):
        sha = hashlib.sha1()
        sha.update(self.dict['info'].__str__().encode())
        return sha.hexdigest()

    def getMessage(self, ):
        # ever when get the messagem, get this properties
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)

        return 'GET /announce HTTP/1.1\n' +\
                'info_hash: ' + str(self.info_hash) + '\n' +\
                'peer_id: ' + self.peer_id + '\n' +\
                'port: ' + self.port + '\n' +\
                'uploaded: ' + str(uploaded) + '\n' +\
                'downloaded: ' + str(downloaded) + '\n' +\
                'left: ' + str(left) + '\r\n\r\n'