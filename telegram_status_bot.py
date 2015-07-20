#!/usr/bin/python -u

from threading import Thread
import socket
import sys, requests, json, schedule, time, psutil

from datetime import timedelta

from secret_conf import *

endpoint = "https://api.telegram.org"

command_send_message = 'sendMessage'
command_read_message = 'getUpdates'

last_update_id = 0

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

def send_message(message, chat_id):
	data = {'text':'----------\nFROM '+socket.gethostname()+':\n\n'+message+'\n----------\n', 'chat_id':str(chat_id) }
	r = requests.post(endpoint+'/'+telegram_token+'/'+command_send_message, data=data)
	return r.json

def send_keep_alive():
	global chat_id_list
	for chat_id in chat_id_list:
		send_message("Buongiorno! Uptime: "+get_uptime(), chat_id )

def send_status(chat_id):
	message = 'UPTIME:\n'+get_uptime() +'\n'
	message += "CPU:\n"+str(psutil.cpu_times_percent()) +'\n'
	message +=  "RAM:\n"+str(psutil.virtual_memory()) +'\n'
	message +=  'DISK:\n'
	for partition in psutil.disk_partitions():
		message += '-  '+ partition.mountpoint +' used: '+ sizeof_fmt(psutil.disk_usage(partition.mountpoint).used)+'/'+sizeof_fmt(psutil.disk_usage(partition.mountpoint).total) +' '+ str(psutil.disk_usage(partition.mountpoint).percent) +'%\n'
	send_message(message, chat_id)

def read_message():
	try:
		global last_update_id, chat_id_list
		data = {'offset':str(last_update_id+1) }
		r = requests.get(endpoint+'/'+telegram_token+'/'+command_read_message, data=data)
		data = json.loads(r.text)
		if 'result' in data:
			for mess in data['result']:
				print('messaggio ricevuto da '+str(mess['message']['chat']['id'])+' : '+ json.dumps(mess['message']) )
				
				if mess['message']['chat']['id'] in chat_id_list:
					if 'text' in mess['message']:
						if mess['message']['text'] == '/status' or mess['message']['text'] == '/status@lampone_bot':
							send_status(mess['message']['chat']['id'])
				
				if last_update_id < mess['update_id']:
					last_update_id = mess['update_id']
	except:
		print ("Unexpected error:", sys.exc_info()[0])
		raise

'''
random_str = ''.join(random.choice( string.ascii_uppercase + string.digits ) for _ in range(16))

thread = Thread( target = SecureServer.start_server, args = (random_str, 8443) )
thread.start()

print ( set_web_hook('lampone.mooo.com', random_str, 8443) )
'''
#self signed cert are NOT supported
#unset_web_hook()

send_message('bot avviato', chat_id_list[0])

schedule.every().day.at("9:30").do( send_keep_alive )

while True:
	read_message()
	schedule.run_pending()
	time.sleep(3)
