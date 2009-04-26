"""

Methods


"""
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import db
import urllib
from utils import simplejson

TINYURL_URL = 'http://tinyurl.com/api-create.php?'
BITLY_URL = 'http://api.bit.ly/shorten?'
BITLY_API_KEY = 'R_4296f0c6d367ada06653899e848f31db' # replace this with your key
BITLY_LOGIN = 'jamtoday' # replace this with your login
TRIM_URL = 'http://api.tr.im/api/trim_url.json?'
ISGD_URL = 'http://is.gd/api.php?'


class ShortLinks():

  def __init__(self, url):
      self.url = url

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

		
