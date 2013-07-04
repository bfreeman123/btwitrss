Brian's Twitter RSS generator
=============================
This is an app engine app that creates rss feeds from twitter user timelines. I built it because twitter shut down their public rss links and now force you to pull data via the API.

Setup
-----
Once you clone the git repo, rename config.py.sample to config.py, and app.yaml.sample to app.yaml. In app.yaml, fill in your app engine identifier. In config.py, fill in your oauth credentials.

OAuth
-----
This app connects to twitter via oauth. In order to set this up, you need a twitter account. Once you have an account, go here to create a twitter app:

https://dev.twitter.com/apps

For the application URL, use your app engine url "https://something.appspot.com".

You can get your Consumer Key and Consumer Secret from the Oauth Settings.

For the Access Token and Secret, click the create my access token button on the bottom of the screen.

Once you have all of this info, copy the values to config.py.

Polling
-------
The cron file has this app polling for new tweets every 15 minutes. It also has it running a purge operation once per day to remove any tweets over 2 days old. These times can be configured in cron.yaml
