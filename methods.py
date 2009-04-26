"""

Methods


"""
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import db
import urllib
from utils import simplejson
from utils.utils import memoize

TINYURL_URL = 'http://tinyurl.com/api-create.php?'
BITLY_URL = 'http://api.bit.ly/shorten?'
BITLY_API_KEY = 'R_4296f0c6d367ada06653899e848f31db' # replace this with your key
BITLY_LOGIN = 'jamtoday' # replace this with your login
TRIM_URL = 'http://api.tr.im/api/trim_url.json?'
ISGD_URL = 'http://is.gd/api.php?'
CLIGS_URL = 'http://cli.gs/api/v1/cligs/create?'

MEMCACHE_TIME = 100000

         
class ShortLinks():


          
  def __init__(self, url):
      self.url = url
      self.response = {}



  def write_response(self):
  	return simplejson.dumps(self.response)

  def getlink(self, method_name):
     from google.appengine.api import memcache
     key = method_name + self.url
     data = memcache.get(key) 
     if data: self.response[method_name] = data
     else: # no cached data
     	this_method = getattr(self, method_name, None)
     	if not this_method: logging.error('no method called %s' % method_name)
     	data = this_method()
     	if data: self.response[method_name] = data
     	memcache.set(key, data, MEMCACHE_TIME)
     	return data


     

  def tinyurl(self):

	self.request_args = {'url':  self.url }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(url = TINYURL_URL + self.formatted_args,
								method = urlfetch.GET)
	return fetch_page.content.strip()
      
        
  def bitly(self):
	self.request_args = {'version':  '2.0.1',
	                     'login': BITLY_LOGIN,
	                     'apiKey': BITLY_API_KEY,
	                     'longUrl': self.url
	                      }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(url = BITLY_URL + self.formatted_args,
								method = urlfetch.GET)
	response = simplejson.loads(fetch_page.content) # um, this is a bad idea in real life
	return response['results'][self.url]['shortUrl']


  def trim(self):
	self.request_args = { 'url': self.url }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(url = TRIM_URL + self.formatted_args,
								method = urlfetch.GET)

	response = simplejson.loads(fetch_page.content) # um, this is a bad idea in real life
	return response['url'].replace('\\/','\\' )


  def isgd(self):
	self.request_args = { 'longurl': self.url }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(url = ISGD_URL + self.formatted_args,
								method = urlfetch.GET)
	return fetch_page.content


  def cligs(self):
	self.request_args = { 'url': self.url }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(url = CLIGS_URL + self.formatted_args,
								method = urlfetch.GET)
	return fetch_page.content
  			

