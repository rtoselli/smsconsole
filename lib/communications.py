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
import appuifw as ui
import appswitch

class bluSocks(object):
	"""Handles the communication via bluetooth with the pc console"""
	
	def __init__(self):
	
		self.serviceName = u'Smsconsole Daemon'
		self.serverSocket = None
		self.channel = None
		self.data = ''
		self.clientAddr = None
		self.clientConn = None
		
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
		
		while self.data[:3] != "\ex":
			
			if not self.clientConn: break
			
			self.data = self.clientConn.recv(4068)
			self.sendMsg()
		
		try:
			self.serverSocket.close()
			self.clientConn.close()
		except:
			pass
			
	def sendMsg(self):
		"""Sends message over the SMS module"""
		print str(self.data)




class sms(object):
	"""Handles the sms sending/receiving"""

	def __init__(self,num=u'',msg=u'',name=u''):
		self.number = num
		self.msg = msg
		self.encoding = '7bit'
		self.name = name

	def sendMsg(self):
		"""Sms sending method"""
		messaging.sms_send(self.number, self.msg, self.encoding, self.smsStatus,self.name)


	def smsStatus(self,status):
		"""Verify the sending status"""
		if status == messaging.ESent:
			ui.note(u"Message sent!","info")
		elif status == messaging.ESendFailed:
			ui.note(u"Error when sending the sms!","error")