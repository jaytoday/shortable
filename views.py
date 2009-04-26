import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

URL_SERVICES = ['tinyurl', 'bitly', 'trim', 'isgd', 'cligs']

class MainPage(webapp.RequestHandler):

	def get(self):	
		template_values = {}
		self.response.out.write(template.render('templates/shortable.html', template_values))


	def get_scoops(self):	
		return False
		

class Shortable(webapp.RequestHandler):

  def get(self):
    if not self.request.get('url'): return self.response.out.write( "dude, where's your url?" )
    # check for cached response would go here
    this_url = self.resolve_url( self.request.get('url') )
    from methods import ShortLinks
    get_links = ShortLinks(this_url)
    for service in URL_SERVICES: 
        try: get_links.getlink(service)
        except: pass 

    self.response.out.write(get_links.write_response())	    

  def resolve_url(self, url):
    from google.appengine.api import urlfetch
    try: fetch_page = urlfetch.fetch(url, follow_redirects=False)
    except: 
        logging.error('unable to fetch url %s' % url)
        return "error"
    try: return fetch_page.headers['location'] # status 301 or 302
    except KeyError: return url # this is final location 
  
  	
