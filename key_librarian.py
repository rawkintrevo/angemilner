from pymongo import MongoClient
from datetime import datetime, timedelta
from time import sleep


def init_api_key(key, provider, max_per_day, s_between_use):
	c= MongoClient()
	db= c['api_keys']
	col= db[provider]
	doc= { '_id': key,	'max_uses_per_day': max_per_day, 's_between_use': s_between_use, 'last_used': datetime.now(), 'uses_today':0 }
	col.save(doc)
	c.close()


def check_out_api_key(provider):
	c= MongoClient()
	db= c['api_keys']
	col= db[provider]
	r = col.aggregate([
			{ '$project': { 'uses_remaining': { '$subtract': ['$max_uses_per_day', '$uses_today'] } , 's_between_use':1, 'last_used':1 } },
			{ '$match' : { 'uses_remaining': { '$gt': 0 }} }, 
			{ '$project': {'ms_bw_use': { '$multiply' : [ '$s_between_use', 1000 ] } , 'last_used':1 } },
			{ '$project' : {'next_use': { '$add': [ '$last_used', '$ms_bw_use' ] }} },
			{ '$project' : {'ms_until_next_use': { '$subtract': [ '$next_use', datetime.now() ] }}},
			{ '$project' : {'s_until_next_use': {'$divide': ['$ms_until_next_use', 1000] } } },
			{ '$sort':  { 's_until_next_use': 1 } },
			{ '$limit': 1 }
	])
	c.close()
	if len(r['result']) > 0:
		s= r['result'][0]['s_until_next_use']
		if s > 0: sleep(s)
		loaner_api_key= r['result'][0]['_id']
		return str(loaner_api_key)
	else: 
		return False
	
def use_api_key(provider, key):
	c= MongoClient()
	db= c['api_keys']
	col= db[provider]
	col.update({'_id':key}, {'$inc': { 'uses_today': 1 }, '$set': { 'last_used': datetime.now() } })
	c.close()

