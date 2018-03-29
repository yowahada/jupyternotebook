# -*- coding:utf-8 -*-
from requests_oauthlib import OAuth1Session
import json, config

# KEY周り
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# タイムラインの取得
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

params = {'screen_name':'YowahaDAs',
          'exclude_replies':True,
          'include_rts':False,
          'count':200
}


res = twitter.get(url, params=params)
timeline = json.loads(res.text)

for tweet in timeline:
    print(tweet["text"])


# if __name__ == "__main__":
#     for j in range(10):
#         res = twitter.get(url, params=params)
#         if res.status_code == 200:
#             print(res.status_code)