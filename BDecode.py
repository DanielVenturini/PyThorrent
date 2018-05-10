# -*-coding:ISO-8859-1 -*-

"""
this decode get one file and decode your full content.
i be this file to decode full .torrent file, but file .torrent has byte and not decode to UTF, the i'm work in this
but to decode file with Bencoding, it's perfect work
use:
------------------------------------------
- from BDecode import BDecode            -
- BDecode('example.torrent/test.decode') -
------------------------------------------

in the future, it's work to full file .torrent
"""

class BDecode:

    def __init__(self, nameFile):
        try:
            self.file = open(nameFile, 'rb')
        except FileNotFoundError:
            print("File not found: " + nameFile)
            return

        #self.keys()
        self.readFileAndDecode()

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
        return self.file.read(1).decode()

    # main def
    def readFileAndDecode(self):

        data = self.read()
        # If the end of the file has been reached, read() will return an empty string ('')
        while(data.__eq__('') == False):

            probabliDic = self.getNextDecode(data)
            print(probabliDic, end=' ')
            data = self.read()


    # when decode string, the first byte is a integer: '4:eggs'
    # but now '17:publisher-webpage' the first and the second byte is integer
    # then i need read bytes until it's integer
    def getFullInteger(self, integer):
        data = self.read()
        while(data.__eq__(':') == False):
            integer += data     # concat the integers
            data = self.read()  # read next byte

        return int(integer)     # return full integer


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


    # def to decode a dictonary. The dictonary is bencode to 'd' following a string bencode,
    # the value is any bencoded type and 'e' to end
    def getDictionaries(self):
        dic = {}

        data = self.read()
        # Dictionaries are encoded as follows: d<bencoded string><bencoded element>e
        while(data.__eq__('e') == False):

            # Note that the keys must be bencoded strings
            key = self.getNextDecode(data)
            value = self.getNextDecode(self.read())

            dic[key] = value
            data = self.read()

        #print("Dictonarie-> ", dic)
        return dic