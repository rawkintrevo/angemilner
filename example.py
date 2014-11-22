import requests
from key_librarian import APIKeyLibrarian

l= APIKeyLibrarian()


## Rate limits on Twitter Search API
## https://dev.twitter.com/rest/reference/get/search/tweets 
REQUEST_PER_15_MIN = 180
DAILY_LIMIT = 24 * 60 / 15 * REQUEST_PER_15_MIN
S_BETWEEN_REQUESTS = float(REQUEST_PER_15_MIN) / (15 * 60) 

PROVIDER = 'twitter_search'

# Create an app at https://apps.twitter.com/
key = { 'api_key'		: 'XXX',
		'api_secret'	: 'YYY',
		'access_token'	: 'ZZZ',
		'access_secret' : '---' }

l.new_api_key(key, PROVIDER, DAILY_LIMIT, S_BETWEEN_REQUESTS )

url= 'https://api.twitter.com/1.1/search/tweets.json'
payload = { 'q' 		: 'apples OR pizza',
			'count'		: 1000 }

key = l.check_out_api_key(PROVIDER)
auth = OAuth1( key['key']['api_key'], key['key']['api_secret'], key['key']['access_token'], key['key']['access_secret'])

r = requests.get(url, params= payload, auth= auth)



