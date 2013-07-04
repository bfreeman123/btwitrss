from google.appengine.ext import ndb
import logging
from google.appengine.api import memcache
import datetime
import tweepy
import config

class Twitter:
  authenticated_api = None
  
  def __init__(self):
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    self.authenticated_api = tweepy.API(auth)
  
  def tweets(self, username):
    return self.authenticated_api.user_timeline(username)
    
  def worker(self):
    query = Account.query()
    accounts = query.fetch(100)
    for account in accounts:
      for tweet in self.tweets(account.username):
        Tweet.create(account, tweet.created_at, tweet.text, tweet.id)

class Base(ndb.Model):
  created_at = ndb.DateTimeProperty(auto_now_add=True)
  updated_at = ndb.DateTimeProperty(auto_now=True)
  
  @staticmethod
  def retrieve(key):
    key = ndb.Key(urlsafe=key)
    return key.get()

class Account(Base):
  username = ndb.StringProperty(required=True, indexed=True)
  
  @staticmethod
  def create(username):
    if not Account.query().filter(Account.username == username).get():
      account = Account(username=username)
      account.put()
      
  def tweets(self):
    return Tweet.query().filter(Tweet.account == self.key).order(Tweet.pub_date).fetch(1000)

class Tweet(Base):
  account = ndb.KeyProperty(kind=Account, required=True)
  pub_date = ndb.DateTimeProperty(indexed=True)
  content = ndb.StringProperty(required=True)
  twitter_id = ndb.IntegerProperty(required=True, indexed=True)
  
  @staticmethod
  def create(account, pub_date, content, twitter_id):
    if twitter_id == None:
      return None
      
    if not Tweet.query().filter(Tweet.twitter_id == twitter_id).get():
      tweet = Tweet(account=account.key, pub_date=pub_date,content=content,twitter_id=twitter_id)
      tweet.put()

