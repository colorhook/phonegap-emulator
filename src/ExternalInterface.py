#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess, json
from PyQt4 import QtCore

class ExternalInterface(QtCore.QObject):

    def __init__(self):
	QtCore.QObject.__init__(self)
	self.commandMap = {}
   
    @QtCore.pyqtSignature("QString", result="QString")
    def call(self, data):
	data = json.loads(str(data))
	command = data["command"]
	output = {}
	output = {"onSuccess": data["onSuccess"], "onFailure": data["onFailure"]}
	if self.commandMap.has_key(command):
		result = self.executeNode(self.commandMap.get(command), data["args"])
		if data.has_key("onSuccess"):
			self.evaluateJavaScript(data["onSuccess"], result)
	else:
		if data.has_key("onFailure"):
			self.evaluateJavaScript(data["onFailure"], 'error')
	return ""
	
    def evaluateJavaScript(self, func, data):
	script = func+"('"+data+"')"
	self.webView.page().mainFrame().evaluateJavaScript(script)

    def executeNode(self, path, arg):
	argv = ""
	for el in arg:
		argv += " "+str(el)
	proc = subprocess.Popen(args='node ' + path + argv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
	out, err = proc.communicate()
	
	return out.strip();
	
    @QtCore.pyqtSignature("QString,QString")
    def addCommand(self, command, nodeFilePath):
	self.commandMap[str(command)] = str(nodeFilePath)

    @QtCore.pyqtSignature("QString")
    def removeCommand(self, command):
	del self.commandMap[str(command)]
    
    @QtCore.pyqtSignature("QString", result="bool")
    def hasCommand(self, command):
	return self.commandMap.has_key(str(command))

    def bindWebView(self, webView):
	self.webView = webView
	webView.page().mainFrame().addToJavaScriptWindowObject("ExternalInterface", self)