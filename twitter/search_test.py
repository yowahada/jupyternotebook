#coding: UTF-8
from requests_oauthlib import OAuth1Session
import json, config


# KEY周り
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

url = "https://api.twitter.com/1.1/search/tweets.json"
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

print("What's search")
keyword = input('>> ')
print('----------------------------------------------------')


params = {'q':keyword, 'count':100}

req = twitter.get(url, params=params)

if req.status_code == 200:
    search_timeline = json.loads(req.text)

    for tweet in search_timeline['statuses']:
        print('>>　' + tweet['text'])
else:
    print("Error: %d" % req.status_code)




# # サクセスコード
# if req.status_code == 200:
#     print("success : " + str(req.status_code))

# for tweet in timeline:
#     print(tweet["text"])

# tweet
# params = {"status":"Hello World"}
# req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)