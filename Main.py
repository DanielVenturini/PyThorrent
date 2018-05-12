# -*- coding:ISO-8859-1 -*-

from BDecode import BDecode
from Intefaces import OpenFile

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
        self.windowMain.connect('destroy', Gtk.main_quit)
        self.windowMain.set_name('PyTorrent')
        self.windowMain.show_all()

        # create the object in the interface
        self.menuopen = self.builder.get_object('menuopen')
        self.menuquit = self.builder.get_object('menuquit')

        #self.menuquit.connect('clicked', Gtk.main_quit)

        Gtk.main()

    def openFile(self, widget):
        self.windowOpenFile = OpenFile()


if __name__.__eq__('__main__'):
    Interface()