#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from SimpleBrowser import SimpleBrowser
from ExternalInterface import ExternalInterface

class MyApplication(QtGui.QApplication):

	def __init__(self, argv):
		QtGui.QApplication.__init__(self, argv)
		self.simpleBrowser = SimpleBrowser()
		self.externalInterface = ExternalInterface()
		self.connect(self.simpleBrowser.ui.webView.page().mainFrame(), QtCore.SIGNAL('javaScriptWindowObjectCleared ()'), self.onObjectClear)
		self.simpleBrowser.show()

	def onObjectClear(self):
		self.externalInterface.bindWebView(self.simpleBrowser.ui.webView)
		

if __name__ == "__main__":
	app = MyApplication(sys.argv)
	sys.exit(app.exec_())