import os
import webapp2
import jinja2
from models import *

class BaseRequest(webapp2.RequestHandler):
  @webapp2.cached_property
  def jinja_environment(self):
    template_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'views'))
    return jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    
  @staticmethod
  def app_factory(routes):
    debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
    config = {}
    return webapp2.WSGIApplication(routes, debug=debug, config=config)
    
  def render(self, page, values):
    template = self.jinja_environment.get_template(page)
    self.response.out.write(template.render(values))
    
