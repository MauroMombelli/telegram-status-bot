from http.server import BaseHTTPRequestHandler,HTTPServer
import ssl, random, string, SecureServer

# This class will handle any incoming request from
# a browser 
class myHandler(BaseHTTPRequestHandler):

	random_str = ''

	def __init__(self, random_str): 
		self.random_str = random_str

	# Handler for the GET requests
	def do_GET(self):
		print   ('Get request received: '+self.path)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(bytes("Hello World !", 'UTF-8'))
		return
	
	def do_POST(self):
		print   ('POST request received: '+self.path)
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}

def start_server(port=8443):
	random_str = ''.join(random.choice( string.ascii_uppercase + string.digits ) for _ in range(16))

	print ( set_web_hook('lampone.mooo.com', random_str, port) )

	handler = myHandler(random_str)

	httpd = HTTPServer(('', port), handler)
	httpd.socket = ssl.wrap_socket (httpd.socket, certfile='certTelegramBot.pem', keyfile='keyTelegramBot.key', server_side=True)
	httpd.serve_forever()
	
	thread = Thread( target = httpd.serve_forever, args = (random_str, port) )
	thread.start()
	
def set_web_hook(url, random, port):
	data = {'url':url+'/'+random+':'+str(port)}
	r = requests.post(endpoint+'/'+token+'/setWebhook', data=data)
	return r.json

def unset_web_hook():
	data = {'url':''}
	r = requests.post(endpoint+'/'+token+'/setWebhook', data=data)
	return r.json