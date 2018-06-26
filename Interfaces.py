# -*- coding:ISO-8859-1 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from defs import defs

OPEN_FILE = 'UI/OpenFile.ui'
UI_FILE = 'UI/Basic_UI.ui'
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


class MainInterface:

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
        self.menuabout = self.builder.get_object('menuabout')
        self.menuopen = self.builder.get_object('menuopen')
        self.menuquit = self.builder.get_object('menuquit')

        # grid of files
        self.gridFile = self.builder.get_object('gridFiles')
        self.line = 2

        Gtk.main()

    def addFile(self, torrentName):
        # name torrent
        labelName = Gtk.Label()
        labelName.set_text(torrentName)

        # percent downloaded
        labelDownloaded = Gtk.Label()
        labelDownloaded.set_text('0%')

        # qtd peers
        labelPeers = Gtk.Label()
        labelPeers.set_text('--')

        # qtd tracker
        labelTracker = Gtk.Label()
        labelTracker.set_text('--')

        self.gridFile.attach(labelName, 0, self.line, 1, 1)
        self.gridFile.attach(labelDownloaded, 1, self.line, 1, 1)
        self.gridFile.attach(labelPeers, 2, self.line, 1, 1)
        self.gridFile.attach(labelTracker, 3, self.line, 1, 1)
        self.gridFile.show_all()

        self.line += 1

    def updatePercent(self, torrentName):
        pass

    def updateTracker(self, torrentName, trackers):
        for line in range(2, self.line):
            label = self.gridFile.get_child_at(0, line)

            if(label.get_text().__eq__(torrentName)):
                labelTracker = self.gridFile.get_child_at(3, line)
                currentPeers = labelTracker.get_text()

                if(currentPeers.__eq__('--')):
                    currentPeers = '0'

                qtdPeer = int(currentPeers) + trackers
                labelTracker.set_text(str(qtdPeer))

    def updatePeer(self, torrentName, peers):
        for line in range(2, self.line):
            label = self.gridFile.get_child_at(0, line)

            if(label.get_text().__eq__(torrentName)):
                labelPeer = self.gridFile.get_child_at(2, line)
                currentPeers = labelPeer.get_text()

                if(currentPeers.__eq__('--')):
                    currentPeers = '0'

                qtdPeer = int(currentPeers) + peers
                labelPeer.set_text(str(qtdPeer))

    def contains(self, torrentName):
        # gridFile.get_child_at(colum, line)
        for line in range(2, self.line):
            label = self.gridFile.get_child_at(0, line)
            if(label.get_text().__eq__(torrentName)):
                return True

        return False

    def createDefsInterface(self):
        return defs(self.addFile, self.updatePercent, self.updateTracker, self.updatePeer, self.contains)

    # menubar -> File -> open
    def openFile(self, widget):
        import openFile
        openFile.openFile(self.createDefsInterface())

    # menubar -> File -> quit
    def quit(self, widget):
        self.windowMain.destroy()

    # menubar -> Help -> about
    def about(self, widget):
        About()