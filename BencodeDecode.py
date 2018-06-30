# -*-coding:ISO-8859-1 -*-

"""
this decode get one file and decode your full content.
The torrent file is perfect decoded using this class.

The encode gets one object and return one string encoded.

use:
---------------------------------------------------------------------
- from BencodeDecode import Decode                                  -
- dec = Decode('path/file.torrent')                                 -
- dec.decodeFullFile()                                              -
- dec.dict['info']['name']                                          -
-                                                                   -
- Or                                                                -
-                                                                   -
- from BencodeDecode import Bencode                                 -
- Bencode().encode([10, 'UTFPR', ['brasil']])                       -
---------------------------------------------------------------------

"""

class Decode:

    def __init__(self, nameFile=''):
        if(not nameFile.__eq__('')):
            try:
                self.file = open(nameFile, 'rb')
            except FileNotFoundError:
                self.file = None
                raise FileNotFoundError

    def decodeFullFile(self):
        if(not self.file):
            print("File not found. Create a new instance of this class with the correct path")
            raise FileNotFoundError

        self.getRawInfo = False
        self.rawinfo = b''
        self.dic = self.getMainDictionarie()

    def decodeBytes(self,respDecoded, respBinary):
        print(respBinary)
        self.file = None
        self.respDecoded = respDecoded
        self.respBinary = respBinary
        self.getRawInfo = False
        self.rawinfo = b''
        self.pos = -1

        return self.getMainDictionarie()

    # read one byte and decode to string
    def read(self):
        # if not file, then is decoded one string

        try:
            if(not self.file):
                self.pos += 1
                return self.respDecoded[self.pos]
        # when in the final of the resp, return -1. The file read(1) from file also returns -1
        except IndexError:
            return -1

        ret = self.file.read(1)
        if(self.getRawInfo):
            self.rawinfo += ret

        # some torrent has coding 'no-utf8'
        return ret.decode('ISO8859-1')


    # since everything is inside a dictionary
    def getMainDictionarie(self):
        data = self.read()
        return self.getNextDecode(data)


    # this def will call the specify def to decode the follows bytes of data
    # data types: byte strings, integers, lists, and dictionaries.
    def getNextDecode(self, data):
        if (data.isdecimal()):
            return self.getString(self.getFullInteger(data))
        elif (data.__eq__('i')):
            return self.getInteger()
        elif (data.__eq__('l')):
            return self.getList()
        elif (data.__eq__('d')):
            return self.getDictionaries()


    # when decode string, the first byte is a integer: '4:eggs'
    # but now '17:publisher-webpage' the first and the second byte is integer
    # then i need read bytes until it's integer
    def getFullInteger(self, integer):
        data = self.read()
        while(data.__eq__(':') == False):
            integer += data     # concat the integers
            data = self.read()  # read next byte

        return int(integer)     # return full integer

    # def to decode string. The first element is a length to string
    def getString(self, length):
        string = ''

        for i in range(0, length):
            string += self.read()

        #print("String-> " + string)
        return string


    # def to decode integer. The bencode is a 'i' 'literal decimal' 'e'
    def getInteger(self):
        integerInString = ''

        data = self.read()
        # All encodings with a leading zero, such as i03e, are invalid
        if(data.__eq__('0')):
            print("Invalide integer: 0")
            return

        # while not equals 'e'
        while(data.__eq__('e') == False):
            integerInString += data
            data = self.read()

        #print("Integer-> " + integerInString)
        return int(integerInString)


    # def to decode a list. The list is bencode to 'l' following bencoding elements and 'e' to end
    def getList(self):
        list = []

        data = self.read()
        while(data.__eq__('e') == False):
            list.append(self.getNextDecode(data))
            data = self.read()

        #print("List-> ", list)
        return list


    # The dictonary is bencode to 'd' following a string bencode,
    # the value is any bencoded type and 'e' to end
    def getDictionaries(self):
        dic = {}

        data = self.read()
        # Dictionaries are encoded as follows:
        # d<bencoded string><bencoded element>e
        while(data.__eq__('e') == False):

            # Note that the keys must be bencoded strings
            key = self.getNextDecode(data)

            # get the mapped info in raw bytes
            if(key.__eq__('info')):
                self.getRawInfo = True

            if(key.__eq__('pieces')):
                value = self.getSHA1ToPieces()

            #elif(not key.__eq__('peers')):
            #    value = self.getNextDecode(self.read())

            elif(not key.__eq__('peers')):
                value = self.getNextDecode(self.read())
            else:
                fullSize = self.getFullInteger(self.read())
                self.pos += 1
                value = self.respBinary[self.pos:self.pos+fullSize]
                self.pos += fullSize
                print("Todo valor aqui: ", value)

            # if is get raw bytes, stop the get raw bytes
            if (key.__eq__('info')):
                self.getRawInfo = False

            dic[key] = value
            data = self.read()

        return dic


    # read the full sequence of SHA-1 pieces
    # this sequence is not UTF-8. That is why is read and converted to hex
    def getSHA1ToPieces(self):
        size = self.getFullInteger('')
        listSHA = []
        seqSHA = ''

        # read all sequence of SHA
        for byte in range(0, size):
            raw = self.file.read(1)

            self.rawinfo += raw
            seqSHA += raw.hex()

            # if the length of sequence is 20,
            # is the end of this sequence
            if(not (byte+1) % 20):
                listSHA.append(seqSHA)
                seqSHA = ''

        return listSHA


#-------------------------------below are the defs to encode one object-------------------------------
class Bencode:

    # this def returns the first object encoded
    def encode(self, object):
        if (str.__instancecheck__(object)):
            return str(object.__len__()) + ':' + object
        elif (int.__instancecheck__(object)):
            return 'i' + str(object) + 'e'
        elif (list.__instancecheck__(object)):
            return self.bencodeList(object)
        elif (dict.__instancecheck__(object)):
            return self.bencodeDictionaries(object)

    def bencodeList(self, object):
        # inicial identify
        response = 'l'
        for ob in object:
            # encode each object
            response += self.encode(ob)

        response += 'e'
        return response

    def bencodeDictionaries(self, object):
        # inicial identify
        response = 'd'
        keyCurrent = ''
        value = None
        for key in list(object.keys()):
            # keys must be string
            keyCurrent += str(key.__len__()) + ':' + key
            mapped = self.encode(object[key])

            response += (keyCurrent + mapped)

            # 'clear' the variables
            keyCurrent = ''
            mapped = None

        response += 'e'
        return response