import os.path, subprocess, string
import multiprocessing as mp

def check_update(timeout=10000):
	pool = mp.Pool(processes = 1)
	result = pool.apply_async(check)
	try:
		return result.get(timeout = timeout)
	except mp.TimeoutError:
		pool.terminate()
		return "Timeout ricevendo gli update"
	else:
		pool.close()
		pool.join()

def check():
	line = ''
	if not db_islocked():
		ris = ''
		with subprocess.Popen('checkupdates', shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
			for line in p.stdout:
				ris += "".join( filter(lambda x: x in string.printable, str(line)) )+"\n";
		return ris
	else:
		return "DB is Locked"

def db_islocked():
	"""Check if we already have a db lock"""
	path_db = '/var/lib/pacman/db.lck'
	if os.path.isfile(path_db):
		return True
	return False