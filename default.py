# -*- coding: utf-8 -*-
"""
Smsconsole
	default.py

Created by Raphael Collares Toselli on 2009-12-30.
All rights reserved.
"""

try:
	import sys
	sys.path.append(u"c:\\data\\python\\lib")
	import appuifw as ui
	from communications import bluSocks as BS
#	from appui import gui
	import e32
	import appswitch
	
except:
	
	import sys
	import traceback
	import e32
	import appuifw

	# panic
	def exithandler(): 
		exitlock.signal()

	appuifw.app.screen = "normal"               
	appuifw.app.focus = None                    
	body = appuifw.Text()
	appuifw.app.body = body                     
	exitlock = e32.Ao_lock()
	appuifw.app.exit_key_handler = exithandler
	appuifw.app.menu = [(u"Exit", exithandler)]
	body.set(unicode("\n".join(traceback.format_exception(*sys.exc_info()))))
	exitlock.wait()
	appuifw.app.set_exit()


if __name__ == '__main__':
	
	# Loads the GUI of the application
#	appgui = gui()
	
	# Starts the bluetooth protocol
	main = BS()
	main.startService()

	# Main Loop 
	while main.data[0] != "\ex": 
		
		if main.data[0] == "-1":
			
			# According to the unix manpage for recv(), when any sort of error occours, the value returned is -1
			
			main.serverSocket.close()
			main.clientConn.close()
			
			#realocate the connection
			main.startService()
	
		else: 
			
			main.recvData()
			print main.data
			
			# Some validations will go here in the near future
			main.sendData()
		
	
	ui.app.set_exit()
	

