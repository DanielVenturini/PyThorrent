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

        # line to insert the name and size in the grid. Start in the line 2
        self.line = 2

        # start UI
        Gtk.main()

    # when click the button to ok read file
    def readFile(self, widget):
        try:
            fileName = self.window.filechooserbutton.get_filename()
            print("Tentando ler o arquivo " + fileName)
            self.decode = BDecode(fileName)
            self.decode.decodeFullFile()
            print("Ja leu")
        except FileNotFoundError:
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

    #def printar tudo

    # verify the main keys of file
    def verifyMainKeys(self):
        # this two keys SHOULD be in the dict
        # if has info, get this, but it's next to verify the keys
        try:
            self.dict['announce']
            self.info = self.dict['info']
            return True
        except KeyError:
            return False


    # verify the keys of info
    def verifyKeysOfInfo(self):
        try:
            # if has this key, the torrent has two or more files
            self.info['files']
            return self.verifyAllKeysOfFiles()
        except KeyError:
            return self.verifyKeysOfFile(self.info)


    # verify each files key in the list of dict
    def verifyAllKeysOfFiles(self):
        try:
            # the keys for dict
            self.info['piece length']
            self.info['pieces']
            self.info['name']

            # the keys for each file
            for file in self.info['file']:
                file['length']
                file['path']

            return True
        except KeyError:
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
            self.info['files']
            return self.printAllFiles()
        except KeyError:
            return self.printOneFile(self.info)

    def printOneFile(self, info):
        size = self.getSize(info['length'])
        name = info['name']

        self.insertInGrid(name, size)


    # dinamic insert in the grid the file name and size
    def insertInGrid(self, file, size):
        label = Gtk.Label()
        label.set_text(file)

        label2 = Gtk.Label()
        label2.set_text(size)

        self.window.gridFile.attach(label, 0, self.line, 1, 1)
        self.window.gridFile.attach(label2, 1, self.line, 1, 1)
        self.window.gridFile.show_all()
        self.line += 1


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
