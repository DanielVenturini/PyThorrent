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
        self.buttomDownload = self.builder.get_object('buttomDownload')
        self.buttomOkReadFile = self.builder.get_object('buttomOkReadFile')
        self.filechooserbutton = self.builder.get_object('filechooserbutton')
        self.gridFile = self.builder.get_object('gridFile')

        self.buttomDownload.set_visible(False)
        # position in the grid to insert the next namefile and size
        self.line = 2

    # clear all content in the grid
    def clearGrid(self):

        while(self.line >= 3):
            self.line -= 1
            self.gridFile.remove_row(self.line)


    # insert name file and size in the grid
    def insertInGrid(self, file, size):
        label = Gtk.Label()
        label.set_text(file)

        label2 = Gtk.Label()
        label2.set_text(size)

        self.gridFile.attach(label, 0, self.line, 1, 1)
        self.gridFile.attach(label2, 1, self.line, 1, 1)
        self.gridFile.show_all()

        self.line += 1

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