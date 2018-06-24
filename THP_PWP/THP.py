# -*- coding:ISO-8859-1 -*-

from requests.utils import quote
from THP_PWP import CommonDef
from threading import Thread
from random import randint
import struct
import socket

class THP(Thread):

    def __init__(self, dict, rawinfo, torrentName=''):
        super(THP, self).__init__()

        self.init(dict, rawinfo, torrentName)

    def init(self, dict, rawinfo, torrentName):
        # if the PyTorrent is on in half download
        # then dict is None
        if(not dict or not rawinfo):
            self.torrentName = torrentName
            return

        self.peers = []
        self.dict = dict
        self.rawinfo = rawinfo
        self.announce = self.dict['announce']
        self.info_hash = self.convertSHA1ToURI()
        self.torrentName = self.dict['info']['name']
        self.lenTorrent = CommonDef.getFullLefFile(self.dict)

        self.addressTracker, self.portTracker = self.getAddressTracker(self.announce)

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

    def run(self):
        self.peer_id = CommonDef.getPeerId()
        self.portTCP = CommonDef.getPort('TCP')
        self.portUDP = CommonDef.getPort('UDP')
        self.num_want = 10

        self.connectAndGetPeerList()

    def convertSHA1ToURI(self):
        return quote(CommonDef.getSHA1(self.rawinfo, hex=False))

    # which event send to server, if none, ''
    def getMessage(self, event=''):
        # ever when get the messagem, get this properties
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)

        # GET /announce?key=value&key=value ... HTTP/1.1 \r\n\r\n
        return ('GET /announce?' +
                'info_hash=' + self.convertSHA1ToURI() + '&' +
                'peer_id=' + self.peer_id + '&' +
                'port=' + str(self.portTCP) + '&' +
                'uploaded=' + str(uploaded) + '&' +
                'downloaded=' + str(downloaded) + '&' +
                'left=' + str(left) + '&' +
                'compact=1' +
                event +
                ' HTTP/1.1\r\n\r\n').encode()

    def connectAndGetPeerList(self):
        # connect with udp socket
        tryList = False
        message = self.getMessage(event='&event=started')
        print(message)
        if(self.announce.startswith('udp://')):
            tryList = self.connectUDP(self.addressTracker, self.portTracker)
        else:
            tryList = self.connectTCP(self.addressTracker, self.portTracker, message)

        if(tryList != False):
            return

        # try announces backup
        for announce in self.dict['announce-list']:
            announce = announce[0]
            address, port = self.getAddressTracker(announce)

            if (announce.startswith('udp://')):
                tryList = self.connectUDP(address, port)
            else:
                tryList = self.connectTCP(address, port, message)

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

            message = self.getPacket1UDP(connection_id, transaction_id, 2)
            s.sendto(message, (addressTracker, portTracker))

            sucess, data = self.checkResponse1UDP(s, transaction_id)
            if(not sucess):
                raise Exception

        except Exception as error:
            print("Erro ao receber em UDP: " + str(error))
            return False

    def connectTCP(self, addressTracker, portTracker, message):
        try:
            print("Conectando TCP: " + addressTracker +":" + str(portTracker))
            s = self.createSocketTCP()
            s.settimeout(0.5)
            s.connect((addressTracker, portTracker))
            s.send(message)
            response = s.recv(1024)

            self.verifyResponse(response)
            return response

        except Exception as error:
            print("Erro ao receber lista do tracker em TCP: " + str(error))
            return False

    def createSocketUDP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('192.168.0.29', self.portUDP))
        self.portUDP = int(s.getsockname()[1])
        s.settimeout(0.5)

        return s

    def createSocketTCP(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        print("PRimeira resposta: ", resp)
        # the len must be 16
        if(len(resp) != 16):
            return False, None

        action, new_transaction_id, connection_id = struct.unpack('!llq', resp)
        if(action != 0 or new_transaction_id != transaction_id):
            return False, None

        print("Tudo certo com transaction id e action")
        return True, connection_id

    def checkResponse1UDP(self, s, transaction_id):
        resp = s.recvfrom(20+((20+6*self.num_want) + (24+6*self.num_want)))[0]
        print("Segunda resposta: ", resp, " Tamanho da resposta: ", len(resp))

        if(len(resp) <= 20):
            return False, None

        action, new_transaction_id, interval, ieechers, seeders = struct.unpack('!lllll', resp[:20])
        if(action != 1 or new_transaction_id != transaction_id):
            return False, None

        print("Tudo certo com transaction id e action")
        print("Recebido: ", action, " ", interval, " ", ieechers, " ", seeders)
        self.recList(resp[20:], seeders)

        return True, resp

    def getPacket1UDP(self, connection_id, transaction_id, event):
        uploaded, downloaded, left = CommonDef.getProperties(self.torrentName, self.lenTorrent)
        print("Porta enviada para o servidor: ", self.portUDP)
        return struct.pack('!qll20s20sQQQIIIiH', connection_id, 1, transaction_id, self.info_hash.encode(), self.peer_id.encode(), uploaded, downloaded, left, event, 0, 0, self.num_want, int(self.portUDP))

    def recList(self, data, seeders):
        print("Vai printar os peers")
        try:

            for i in range(0, seeders):
                ip = self.getFullIP(struct.unpack('BBBB', data[i*6:((i*6)+4)]))
                port = struct.unpack('!h', data[((i*6)+4):((i*6)+4)+2])
                print(ip, ":", port[0])

        except Exception as ex:
            print("Error em printar a lista: " + str(ex))

        print("Jah printou")

    def getFullIP(self, data):
        return str(data[0])+'.'+str(data[1])+'.'+str(data[2])+'.'+str(data[3])

    def verifyResponse(self, response):
        method = response[:12]
        print("Recebeu a seguinte resposta: ", method)