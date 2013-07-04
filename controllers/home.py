from controllers.base import *
import datetime
from google.appengine.api import taskqueue

class MainPage(BaseRequest):
  def get(self):
    accounts = Account.query().order(Account.username).fetch(1000)
    self.render('index.html', {'accounts': accounts})
    
class CreateTwitter(BaseRequest):
  def post(self):
    Account.create(self.request.get('username'))
    self.redirect('/')
    
class GetTweets(BaseRequest):
  def post(self):
    twitter = Twitter()
    twitter.worker()
    
class SpawnWorker(BaseRequest):
  def get(self):
    taskqueue.add(url='/get_tweets', params={})
    
class Prune(BaseRequest):
  def get(self):
    taskqueue.add(url='/prune_worker', params={})
    
class PruneWorker(BaseRequest):
  def post(self):
    tweets = Tweet.query().fetch(1000)
    
    cutoff = datetime.datetime.now() - datetime.timedelta(days=2)
    for tweet in tweets:
      if tweet.created_at < cutoff:
        tweet.key.delete()

routes = [('/', MainPage),
          ('/create_twitter', CreateTwitter),
          ('/get_tweets', GetTweets),
          ('/spawn_worker', SpawnWorker),
          ('/prune', Prune),
          ('/prune_worker', PruneWorker)]

app = BaseRequest.app_factory(routes)
