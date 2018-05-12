# -*- coding:ISO-8859-1 -*-

from BDecode import BDecode

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

UI_FILE = 'UI/Basic_UI.ui'

class Interface:

    def __init__(self):
        self.builder = Gtk.Builder()

        # create the graphic interface from a file
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        # create the UI
        self.windowMain = self.builder.get_object('windowMain')
        self.windowMain.show_all()
        self.windowMain.connect('destroy', Gtk.main_quit)
        self.windowMain.set_name('PyTorrent')

        # create the object in the interface
        self.buttomReadFile = self.builder.get_object('buttomReadFile')
        self.entryReadFile = self.builder.get_object('entryReadFile')

        Gtk.main()

    def delFileNotFoundError(self, widget):
        print("Clicado")
        self.windowNotFound.destroy()

    def fileNotFoundError(self):
        windowNotFound = self.builder.get_object('windowNotFound')
        windowNotFound.show_all()
        windowNotFound.set_name('Error')

        self.windowNotFound = windowNotFound

    # this def is call when the buttomReadFile is clicked
    def clickReadFile(self, widget):
        # get the name of file
        fileName = self.entryReadFile.get_text()
        if(fileName.__eq__('')):
            print('No file name')
            return

        try:
            BDecode(fileName).decodeFullFile()
        except FileNotFoundError:
            self.fileNotFoundError()




if __name__.__eq__('__main__'):
    Interface()