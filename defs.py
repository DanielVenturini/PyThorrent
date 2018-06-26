# -*- coding:ISO-8859-1 -*-

# this class is only to pack all callbacks def to interface
class defs:

    def __init__(self, addFile, updatePercent, updateTracker, updatePeer, contains):
        self.addFile = addFile
        self.contains = contains
        self.updatePeer = updatePeer
        self.updatePercent = updatePercent
        self.updateTracker = updateTracker