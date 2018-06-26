# -*- coding:ISO-8859-1 -*-

from requests.utils import quote
from BencodeDecode import Decode
from THP_PWP import CommonDef
from threading import Thread
import socket

class TCPConnection(Thread):

    def __init__(self, torrentName, peer_id, port, announceList, num_want, rawinfo, lenTorrent, defsInterface):
        Thread.__init__(self)

        self.peers = []
        self.port = port
        self.peer_id = peer_id
        self.num_want = num_want
        self.rawinfo = rawinfo
        self.lenTorrent = lenTorrent
        self.torrentName = torrentName
        self.announceList = announceList
        self.defsInterface = defsInterface

    def start(self):
        # try announces backup
        message = self.getMessage(event='&event=started')
        print(message)
        for announce in self.announceList:
            announce = announce[0]

            if (announce.startswith('http://')):
                address, port = self.getAddressTracker(announce)
                tryList = self.connectTCP(address, port, message)
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


    def convertSHA1ToURI(self):
        return quote(CommonDef.getSHA1(self.rawinfo, hex=False))


    def verifyResponse(self, response):
        method = response[:12].decode()
        #print("Recebeu a seguinte resposta: ", method)

        if(method.__eq__('HTTP/1.1 200')):
            #print(response[12:])
            # to body
            return self.getPeersTCP(response[response.index('\r\n\r\n'.encode())+4:])
        else:
            return False


    # which event send to server, if none, ''
    def getMessage(self, event=''):
        # ever when get the messagem, get this properties
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)

        # GET /announce?key=value&key=value ... HTTP/1.1 \r\n\r\n
        return ('GET /announce?' +
                'info_hash=' + self.convertSHA1ToURI() + '&' +
                'peer_id=' + self.peer_id + '&' +
                'port=' + str(self.port) + '&' +
                'uploaded=' + str(uploaded) + '&' +
                'downloaded=' + str(downloaded) + '&' +
                'left=' + str(left) + '&' +
                'compact=1' +
                event +
                ' HTTP/1.1\r\n\r\n').encode()


    def connectTCP(self, addressTracker, portTracker, message):
        try:
            print("Conectando TCP: " + addressTracker +":" + str(portTracker))
            s = self.createSocketTCP()
            s.settimeout(0.5)
            s.connect((addressTracker, portTracker))
            s.send(message)
            response = s.recv(1024)

            if(self.verifyResponse(response)):
                # save the tracker
                CommonDef.setTracker(self.torrentName, 'http://'+addressTracker+':'+str(portTracker))
                self.defsInterface.updateTracker(self.torrentName, 1)

            return response

        except Exception as error:
            print("Erro ao receber lista do tracker em TCP: " + str(error))
            return False


    def createSocketTCP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def getPeersTCP(self, data):
        try:
            dic = Decode().decodeBytes(data)
            print(dic['peers'])
        except Exception as ex:
            print('Erro na hora de recuperar os peers em TCP: ' + str(ex))