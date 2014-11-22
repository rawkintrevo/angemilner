from pymongo import MongoClient
from datetime import datetime, timedelta
from time import sleep


class APIKeyLibrarian:
	def __init__(self,db_name='api_keys', **kwargs ):
		self.c = MongoClient(**kwargs)
		self.db = self.c['api_keys']
	
	def new_api_key(self, key, provider, max_per_day, s_between_use):
		col= self.db[provider]
		doc= { 	'key': key,	
				'max_uses_per_day': max_per_day, 
				's_between_use': s_between_use, 
				'last_used': datetime.now(), 
				'uses_today':0 }
		col.create_index('key')
		col.save(doc)

	def check_out_api_key(self, provider):
		col= self.db[provider]
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
		if len(r['result']) > 0:
			s= r['result'][0]['s_until_next_use']
			if s > 0: sleep(s)
			loaner_api_key= col.find_one({'_id': r['result'][0]['_id']})['key']
			self.use_api_key(provider, loaner_api_key)
			return {'key': loaner_api_key}
		else: 
			return {}

	def use_api_key(self, provider, key):
		col= self.db[provider]
		self.reset_key(provider, key)
		silent = col.update({'key':key}, {'$inc': { 'uses_today': 1 }, '$set': { 'last_used': datetime.now() } })

	def reset_key(self, provider, key):
		col= self.db[provider]
		doc = col.find_one({'key':key})
		if (datetime.now() - doc['last_used']) > timedelta(days=1):
			doc['uses_today'] = 0

	def set_value(self, provider, key, values):
		col= self.db[provider]
		doc= col.find_one({'key': key})
		new_doc = dict(doc.items() + values.items() )
		col.save(new_doc) 
