# -*-coding:ISO-8859-1 -*-

"""
this decode get one file and decode your full content.
The torrent file is perfect decoded using this class.

use:
--------------------------------------------------------------------
- from BDecode import BDecode                                      -
- BDecode('example.torrent/onlyonefile.torrent').decodeFullFile()  -
--------------------------------------------------------------------

"""

class BDecode:

    def __init__(self, nameFile):
        try:
            self.file = open(nameFile, 'rb')
        except FileNotFoundError:
            self.file = None
            raise FileNotFoundError

    def decodeFullFile(self):
        if(not self.file):
            print("File not found. Create a new instance of this class with the correct path")
            raise FileNotFoundError

        #self.keys()
        self.dict = self.getMainDictionarie()

    # the def is only to show the variables of the metainfo
    def keys(self):
        # the keys of metainfo
        self.creationdate = "THISVALUEISOPTIONAL"
        self.announcelist = "THISVALUEISOPTIONAL"
        self.createdby = "THISVALUEISOPTIONAL"
        self.announce = "THISVALUEISREQUERID"
        self.info = "THISVALUEISADICTIONARY"
        self.comment = "THISVALUEISOPTIONAL"

    # read one byte and decode to string
    def read(self):
        # some torrent has coding 'no-utf8'
        return self.file.read(1).decode('ISO8859-1')


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
            if(key.__eq__('pieces')):
                value = self.getSHA1ToPieces()
            else:
                value = self.getNextDecode(self.read())

            dic[key] = value
            data = self.read()

        #print("Dictonarie-> ", dic)
        return dic


    # read the full sequence of SHA-1 pieces
    # this sequence is not UTF-8. That is why is read and converted to hex
    def getSHA1ToPieces(self):
        size = self.getFullInteger('')
        listSHA = []
        seqSHA = ''

        # read all sequence of SHA
        for byte in range(0, size):
            seqSHA += self.file.read(1).hex()

            # if the length of sequence is 20,
            # is the end of this sequence
            if(not (byte+1) % 20):
                listSHA.append(seqSHA)
                seqSHA = ''

        return listSHA