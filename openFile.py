# -*- coding:ISO-8859-1 -*-

from Interfaces import openFileInterface
from BDecode import BDecode

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class openFile:

    def __init__(self):
        self.window = openFileInterface()

        # add the event clicked to execute the def readFile
        self.window.buttomOkReadFile.connect('clicked', self.readFile)
        print("ja foi pra clicar")

        # start UI
        Gtk.main()

    # when click the button to ok read file
    def readFile(self, widget):
        self.window.clearGrid()

        try:
            fileName = self.window.filechooserbutton.get_filename()
            print("Tentando ler o arquivo " + fileName)
            self.decode = BDecode(fileName)
            self.decode.decodeFullFile()
            print("Ja leu")
        except FileNotFoundError:
            print("Erro no readFile")
            self.insertInGrid('Arquivo nao encontrado.', '-')
            return

        self.processFile()


    # check all keys in the file
    def processFile(self):
        self.dict = self.decode.dict

        if(not self.verifyMainKeys()):
            self.insertInGrid('Arquivo invalido', '-')
            return
        elif(not self.verifyKeysOfInfo()):
            self.insertInGrid('Arquivo invalido', '-')
            return

        self.printFiles()

    # each position in the listPath is one path at final file
    def getFullPath(self, listPath):

        fullPath = ''
        for path in listPath:
            fullPath += ('/' + path)

        return fullPath

    #def printar tudo
    def printAllFiles(self, listOfFiles):
        # the keys for each file
        for file in listOfFiles:
            self.insertInGrid(self.getFullPath(file['path']), self.getSize(file['length']))

    # verify the main keys of file
    def verifyMainKeys(self):
        # this two keys SHOULD be in the dict
        # if has info, get this, but it's next to verify the keys
        try:
            self.dict['announce']
            self.info = self.dict['info']
            return True
        except KeyError:
            print("Erro no mainKeys")
            return False


    # verify the keys of info
    def verifyKeysOfInfo(self):
        try:
            # if has this key, the torrent has two or more files
            self.info['files']
            return self.verifyAllKeysOfFiles()
        except KeyError:
            print("Erro no verifyKeysOfInfo")
            return self.verifyKeysOfFile(self.info)


    # verify each files key in the list of dict
    def verifyAllKeysOfFiles(self):
        try:
            # the keys for dict
            self.info['piece length']
            self.info['pieces']
            self.info['name']

            # the keys for each file
            for file in self.info['files']:
                file['length']
                file['path']

            return True
        except Exception as error:
            print("Erro no verifyAllKeysOfFiles: " + str(error))
            return False


    # verify if the file has all keys
    def verifyKeysOfFile(self, file):
        try:
            file['piece length']
            file['length']
            file['pieces']
            file['name']
            return True
        except KeyError:
            print("Erro no verifyKeysOfFile")
            return False

    # insert all file and size in the grid
    def insertFilesInGrid(self):
        try:
            # torrent with two files or more
            files = self.decode.dict['info']['files']
        except:
            # torrent with only one file
            file = self.decode.dict['info']

    def printFiles(self):
        try:
            # if has this key, the torrent has two or more files
            return self.printAllFiles(self.info['files'])
        except KeyError:
            return self.printOneFile(self.info)

    def printOneFile(self, info):
        size = self.getSize(info['length'])
        name = info['name']

        self.insertInGrid(name, size)


    # dinamic insert in the grid the file name and size
    def insertInGrid(self, file, size):
        self.window.insertInGrid(file, size)


    # 'translate' the bytes of file to a real size: kB, MB, GB
    def getSize(self, size):
        size = int(size)
        if (size == -1):
            return '---'

        sizeFull = ""
        if (size < 1000):
            return str(size) + ' bytes'
        elif (size < 1e+6):
            return str(int(size / 1000)) + ',' + str(int((size % 1000) / 100)) + ' kB'
        elif (size < 1e+9):
            return str(int(size / 1e+6)) + ',' + str(int((size % 1e+6) / 1e+5)) + ' MB'
        else:
            return str(int(size / 1e+9)) + ',' + str(int((size % 1e+9) / 1e+8)) + ' GB'
