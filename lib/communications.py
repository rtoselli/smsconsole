# -*- coding: utf-8 -*-
"""
Smsconsole
	communications.py

Created by Raphael Collares Toselli on 2009-12-30.
All rights reserved.

	TODO:
			Multiple messages
			Multiple numbers
			Contacts Integration

"""

import btsocket as bt
import messaging
import appuifw as ui
import appswitch

class bluSocks(object):
	"""Handles the communication via bluetooth with the pc console"""
	
	def __init__(self):
	
		self.serviceName = u'Smsconsole Daemon'
		self.serverSocket = None
		self.channel = None
		self.data = [""]
		self.clientAddr = None
		self.clientConn = None
		self.sms = sms()
		
	def startService(self):
		"""Initiates the bluetooth sockets and listen for a connection"""
		
		self.serverSocket = bt.socket(bt.AF_BT,bt.SOCK_STREAM)
		
		#Gets a free channel for communication
		self.channel = bt.bt_rfcomm_get_available_server_channel(self.serverSocket)
		
		#Binds the socket to that channel and listen for connection
		self.serverSocket.bind(("",self.channel))
		bt.bt_advertise_service( self.serviceName,
                              self.serverSocket,
		                      True,
		                      bt.RFCOMM )
		
		bt.set_security(self.serverSocket, bt.AUTHOR | bt.AUTH )
		self.serverSocket.listen(1)
		
		#Forking into the background
		appswitch.switch_to_fg(u'PythonScriptShell')
		ui.note(u"SmsConsole: Waiting for connections","info")
		appswitch.switch_to_bg(u'PythonScriptShell')
		
		self.clientConn,self.clientAddr = self.serverSocket.accept()
		
		appswitch.switch_to_fg(u'PythonScriptShell')
		ui.note(u"Client %s Connected" % (self.clientAddr), "info")
		appswitch.switch_to_bg(u'PythonScriptShell')
		
	def recvData(self):
		"""Recieves data from the socket"""
		self.data = str(self.clientConn.recv(4068)).rsplit("|")
			
	def sendData(self):
		"""docstring for sendData"""
		if len(self.data) == 4 and self.data[3] == "1":
			appswitch.switch_to_fg(u'PythonScriptShell')
			ui.note(u"Sending msg: %s" % (self.data[1]),"info")
			appswitch.switch_to_bg(u'PythonScriptShell')
		
			self.sms.name = u"%s" % (self.data[2])
			self.sms.msg = u"%s" % (self.data[1])
			self.sms.number = u"%s" % (self.data[0])
			self.sms.sendMsg()
			

class sms(object):
	"""Handles the sms sending/receiving"""

	def __init__(self):
		self.number = None
		self.msg = None
		self.encoding = '7bit'
		self.name = None

	def sendMsg(self):
		"""Sms sending method"""
		messaging.sms_send(self.number, self.msg, self.encoding, self.smsStatus,self.name)


	def smsStatus(self,status):
		"""Verify the sending status"""
		if status == messaging.ESent:
			ui.note(u"Message sent!","info")
		elif status == messaging.ESendFailed:
			ui.note(u"Error when sending the sms!","error")