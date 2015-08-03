#!/usr/bin/python -u

import schedule, time, psutil

from datetime import timedelta

from secret_conf import *
from telegram_api import *
from pacman_status import *

def get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))
	
	return uptime_string

def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

def send_keep_alive(mess = 'Buongiorno'):
	global chat_id_list
	for chat_id in chat_id_list:
		send_message(mess+"! Uptime: "+get_uptime()+"\nAggiornamenti disponibili:\n"+check_update(), chat_id )

def send_status(chat_id):
	message = 'UPTIME:\n'+get_uptime() +'\n'
	message += "CPU:\n"+str(psutil.cpu_times_percent()) +'\n'
	message +=  "RAM:\n"+str(psutil.virtual_memory()) +'\n'
	message +=  'DISK:\n'
	for partition in psutil.disk_partitions():
		message += '-  '+ partition.mountpoint +' used: '+ sizeof_fmt(psutil.disk_usage(partition.mountpoint).used)+'/'+sizeof_fmt(psutil.disk_usage(partition.mountpoint).total) +' '+ str(psutil.disk_usage(partition.mountpoint).percent) +'%\n'
	send_message(message, chat_id)

'''
random_str = ''.join(random.choice( string.ascii_uppercase + string.digits ) for _ in range(16))

thread = Thread( target = SecureServer.start_server, args = (random_str, 8443) )
thread.start()

print ( set_web_hook('lampone.mooo.com', random_str, 8443) )
'''
#self signed cert are NOT supported
#unset_web_hook()

#for chat_id in chat_id_list:
#	send_message('bot avviato', chat_id)

send_keep_alive('Bot avviato')

schedule.every().day.at("9:30").do( send_keep_alive )

while True:
	read_message()
	schedule.run_pending()
	time.sleep(3)
