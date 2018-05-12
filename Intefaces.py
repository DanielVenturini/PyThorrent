# -*- coding:ISO-8859-1 -*-

from BDecode import BDecode

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

OPEN_FILE = 'UI/OpenFile.ui'

class OpenFile:

    def __init__(self):
        self.builder = Gtk.Builder()

        # create the graphic interface from a file
        self.builder.add_from_file(OPEN_FILE)
        self.builder.connect_signals(self)

        # create the UI
        self.windowOpenFile = self.builder.get_object('windowOpenFile')
        self.windowOpenFile.connect('destroy', Gtk.main_quit)
        self.windowOpenFile.set_name('OpenFile')
        self.windowOpenFile.show_all()

        # create the object in the interface
        #self.buttomDownloadFile = self.builder.get_object('buttomDownloadFile')
        #self.buttomOKReadFile = self.builder.get_object('buttomOkReadFile')
        self.entryReadFile = self.builder.get_object('entryReadFile')
        self.labelFileName = self.builder.get_object('labelFileName')
        self.labelSize = self.builder.get_object('labelSize')

        self.fileExists = False
        Gtk.main()

    def oKReadFile(self, widget):
        try:
            fileName = self.entryReadFile.get_text()
            print("Tentando ler o arquivo " + fileName)
            self.decode = BDecode(fileName)
            self.decode.decodeFullFile()
            self.fileExists = True
            print("Ja leu")
        except FileNotFoundError:
            self.labelFileName.set_text('Arquivo nao encontrado.')
            return

        try:
            # file is true
            self.labelFileName.set_text(self.decode.dict['info']['name'])
            self.labelSize.set_text(self.getSize(self.decode.dict['info']['length']))
        except KeyError:
            print("Erro de chave")
            pass

        return


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