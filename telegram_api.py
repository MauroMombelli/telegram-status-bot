import socket, requests, json, sys

from secret_conf import *

endpoint = "https://api.telegram.org"

command_send_message = 'sendMessage'
command_read_message = 'getUpdates'

last_update_id = 0

def send_message(message, chat_id):
	global telegram_token
	data = {'text':'----------\nFROM '+socket.gethostname()+':\n\n'+message+'\n----------\n', 'chat_id':str(chat_id) }
	r = requests.post(endpoint+'/'+telegram_token+'/'+command_send_message, data=data)
	return r.json

def read_message():
	try:
		global last_update_id, chat_id_list, telegram_token
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