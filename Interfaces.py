# -*- coding:ISO-8859-1 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

OPEN_FILE = 'UI/OpenFile.ui'
ABOUT = 'UI/About.ui'

class openFileInterface:

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
        self.buttomOkReadFile = self.builder.get_object('buttomOkReadFile')
        self.entryReadFile = self.builder.get_object('entryReadFile')
        self.gridFile = self.builder.get_object('gridFile')

class About:

    def __init__(self):
        self.builder = Gtk.Builder()

        # create the graphic interface from a file
        self.builder.add_from_file(ABOUT)
        self.builder.connect_signals(self)

        # create the UI
        self.windowAbout = self.builder.get_object('windowAbout')
        self.windowAbout.set_name('PyTorrent About')
        self.windowAbout.show_all()