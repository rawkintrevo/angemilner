angemilner
=================

The Ghost of Ange Milner sets up a library of your API keys using MongoDB.  Then everytime you need to make an API call, she checks out the key that has been resting the longest/ has the most remaining calls before it hits the daily rate limit.

Spirit of the package
---------------------
When scraping the web for information I'm constantly getting rate limited.  This is in no small part due to the fact that I'm cheap and prefer to use a collection of low limit developer API keys to buying a full service key. Aside from that there are some legitamite reasons to use this as well.  (TODO think of legitimate reason and put it here). 

You might think, "why use MongoDB, that is a lot of over head and you could achieve the same result with a python dictionary." You might think that, and you would be wrong.  Not really wrong, but in my experience scripts that make API calls all day long have a tendancy to fail. If the whole program crashes you have no idea how much of a key you have used.  Also this allows multiple processes to use a central accounting of key useage.  There is probably some way to achieve this result with less over head, and if you're that worried about over head and you think of a way, go write your own program. 

In list form:

1. Key useage data is persistent through multiple sessions of Python and robust to crashing.

2. A central source of key useage data wholey outside of the Python session makes things easier when you have multiple programs trying to access the same set of API keys. 

Installation
-------------
Pip is the way to install angemilner.  Just give it the 'ol 
```
pip install angemilner
```

Dependencies
-------------
This package requires pymongo, datetime, and time

For those who know a little Mongo...
------------------------------------

All that is going on here is a database (by default named 'api_keys') is created.  Each service has it's own collection.  In that collection each API key is a document, with additional fields containing information such as when the key was last used and how many time the key has been used today.  When you check out a key, it does a little Mongo aggregation to return a key that A) hasn't hit its daily rate limit and B) of has had the most time since it was last used. 

If no key is available, it finds the key that will be available next and sleeps until that key is available. That makes API scraping a nice 'fire and forget' process. 



