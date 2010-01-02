# -*- coding: utf-8 -*-
"""
Smsconsole
	default.py

Created by Raphael Collares Toselli on 2009-12-30.
All rights reserved.
"""

try:
	import sys
	sys.path.append(u"c:\\data\\python")
	import appuifw as ui
	from communications import bluSocks as BS
	import e32
	
except:
	
	import sys
	import traceback
	import e32
	import appuifw

	#Modo panic
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
	
	
	main = BS()
	
	main.startService()
	main.recvData()
	ui.app.set_exit()
	

