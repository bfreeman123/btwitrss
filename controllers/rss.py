from controllers.base import *
import datetime
import PyRSS2Gen
    
class GetRss(BaseRequest):
  def get(self):
    username = self.request.get('username')
    account = Account.query().filter(Account.username == username).get()
    tweets = []
    for tweet in account.tweets():
      item = PyRSS2Gen.RSSItem(
        title = tweet.content,
        link = "https://twitter.com/" + username + "/status/" + str(tweet.twitter_id),
        description = tweet.content,
        guid = PyRSS2Gen.Guid(str(tweet.twitter_id)),
        pubDate = tweet.pub_date
      )
      tweets.append(item)
    
    rss = PyRSS2Gen.RSS2(
      title = "Tweets for " + username,
      link = "https://twitter.com/" + username,
      description = "Tweets for " + username,

      lastBuildDate = datetime.datetime.utcnow(),

      items = tweets
    )
    self.response.headers['Content-Type'] = 'text/xml'
    self.response.write(rss.to_xml())

routes = [('/rss', GetRss)]

app = BaseRequest.app_factory(routes)
