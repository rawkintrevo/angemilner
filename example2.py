import requests
from angemilner import APIKeyLibrarian

l= APIKeyLibrarian()
PROVIDER = 'google_places'

## To generate keys for google go to https://console.developers.google.com
google_keys = [	'xxx',
				'yyy']


DAILY_LIMIT = 1000  
""" 
Google Places Free Limit, 100,000 if you have a card on file. 
Divide by 10 if you are doing text searches """

S_BETWEEN_REQUESTS = 0.1 # Technically no limit

for key in google_keys:
	l.new_api_key(key, PROVIDER, DAILY_LIMIT, S_BETWEEN_REQUESTS )


keywords = ['pizza', 'chinese', 'sandwiches', 'beer' ]
location = '41.9075,-87.6769' # Wicker Park

for q in keywords:
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	key = l.check_out_api_key(PROVIDER)['key']
	payload = {	'key' 		: key,
				'location'	: location, 
				'radius'	: 1000, 
				'name'		: q,
				'types'		: 'restaurant' }
	r = requests.get(url, params= payload) 
	print key	
	print len(r.json()['results'])
