#coins-e api

import requests, json

from operator import itemgetter

#get exchange and level

def getLevel(exchange_a, exchange_b, bids, asks):
	r = requests.get('https://www.coins-e.com/api/v2/market/'+exchange_a+'_'+exchange_b+'/depth/', verify=False) #so bad, need to make it work
	data = json.loads(r.text)
	
	#print('bids')
	for bid in data['marketdepth']['bids']:
		bids.append( ( str(bid['r']), str(bid['q']), 'coins-e.com' ) )
		#print(bid['r'], ' ', bid['q'])
		
	#print('asks')
	for ask in data['marketdepth']['asks']:
		asks.append( ( str(ask['r']), str(ask['q']), 'coins-e.com' ) )
		#print(ask['r'], ' ', ask['q'])

def getLevelBter(exchange_a, exchange_b, bids, asks):
	r = requests.get('http://data.bter.com/api/1/depth/'+exchange_a+'_'+exchange_b) #so bad, need to make it work
	data = json.loads(r.text)
	
	#print('bids')
	for bid in data['bids']:
		bids.append( ( str(bid[0]), str(bid[1]), 'bter.com' ) )
		#print(bid[0], ' ', bid[1])
		
	#print('asks')
	for ask in data['asks']:
		asks.append( ( str(ask[0]), str(ask[1]), 'bter.com' ) )
		#print(ask[0], ' ', ask[1])

#---------------------------------------

bids = []
asks = []

print('DOGE/BTC')

getLevel('DOGE', 'BTC', bids, asks)
getLevelBter('doge', 'btc', bids, asks)

bids = sorted(bids, key=itemgetter(1), reverse=True) #first order by quantity
bids = sorted(bids, key=itemgetter(0), reverse=True) #now sort by price, as ordering in python is stable

asks = sorted(asks, key=itemgetter(1), reverse=True) #first order by quantity
asks = sorted(asks, key=itemgetter(0), reverse=False) #now sort by price, as ordering in python is stable

print('bids')
for v in bids:
	print(v[0], ' ', v[1], ' ', v[2])
	
print('asks')
for v in asks:
	print(v[0], ' ', v[1], ' ', v[2])

#---------------------------------------

bids_doge_usd = []
asks_doge_usd = []

print('DOGE/USD')

getLevelBter('doge', 'usd', bids_doge_usd, asks_doge_usd)

bids_doge_usd = sorted(bids_doge_usd, key=itemgetter(1), reverse=True) #first order by quantity
bids_doge_usd = sorted(bids_doge_usd, key=itemgetter(0), reverse=True) #now sort by price, as ordering in python is stable

asks_doge_usd = sorted(asks_doge_usd, key=itemgetter(1), reverse=True) #first order by quantity
asks_doge_usd = sorted(asks_doge_usd, key=itemgetter(0), reverse=False) #now sort by price, as ordering in python is stable

print('bids')
for v in bids_doge_usd:
	print(v[0], ' ', v[1], ' ', v[2])
	
print('asks')
for v in asks_doge_usd:
	print(v[0], ' ', v[1], ' ', v[2])

#---------------------------------------

bids_btc_usd = []
asks_btc_usd = []

print('BTC/USD')

getLevelBter('btc', 'usd', bids_btc_usd, asks_btc_usd)

bids_btc_usd = sorted(bids_btc_usd, key=itemgetter(1), reverse=True) #first order by quantity
bids_btc_usd = sorted(bids_btc_usd, key=itemgetter(0), reverse=True) #now sort by price, as ordering in python is stable

asks_btc_usd = sorted(asks_btc_usd, key=itemgetter(1), reverse=True) #first order by quantity
asks_btc_usd = sorted(asks_btc_usd, key=itemgetter(0), reverse=False) #now sort by price, as ordering in python is stable

print('bids')
for v in bids_btc_usd:
	print(v[0], ' ', v[1], ' ', v[2])
	
print('asks')
for v in asks_btc_usd:
	print(v[0], ' ', v[1], ' ', v[2])

#---------------------------------------

print ( bids[0][0], ' ', bids_doge_usd[0][0], ' ', bids_btc_usd[0][0] )
print ( asks[0][0], ' ', asks_doge_usd[0][0], ' ', asks_btc_usd[0][0] )

