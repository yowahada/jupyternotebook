from requests_oauthlib import OAuth1Session
import json, config, time, datetime, re, csv, sys, traceback

# KEY周り
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

#　認証
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# search関数
def getTweetData(search_word, max_id, since_id):
    global twitter
    url = 'https://api.twitter.com/1.1/search/tweets.json'

    # pamams settings
    params = {
        'q':search_word,
        'count':'200',
    }

    if max_id != -1:
        params['max_id'] = max_id
    if since_id != -1:
        params['since_id'] = since_id

    req = twitter.get(url, params=params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        metadata = timeline['search_metadata']
        statuses = timeline['statuses']
        limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
        reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0
        return {
            "result":True,
            "metadata":metadata,
            "statuses":statuses,
            "limit":limit,
            "reset_time":datetime.datetime.fromtimestamp(float(reset)),
            "reset_time_unix":reset
        }
    else:
        print("Error: %d" % req.status_code)
        return {
            "result":False,
            "status_code":req.status_code
        }

def now_unix_time():
    return time.mktime(datetime.datetime.now().timetuple())

# get tweet
sid = -1
mid = -1
count = 0
res = None

while(True):
    try:
        count = count +1
        sys.stdout.write("%d, "% count)
        kw = u'リノベーション'

        res = getTweetData(kw, max_id=mid, since_id=sid)

        # 失敗したら終了
        if res['result']==False:
            print("status_code", res['status_code'])
            break

        # sleep処理と書き込み処置
        if int(res['limit']) == 0:# 回数制限に達したので休憩
            diff_sec = int(res['reset_time_unix']) - now_unix_time()
            print("sleep %d sec" % (diff_sec+5))
            if diff_sec > 0:
                time.sleep(diff_sec+5)
        else:
            if len(res['statuses'])==0:
                sys.stdout.write("statuses is none. ")
                break
            elif 'next_results' in res['metadata']:
                print('is_next_results')
                with open("tweet(kw_" + kw +").csv", "a") as f:
                    writer = csv.writer(f)
                    for i in range(len(res['statuses'])):
                        writer.writerow([res['statuses'][i]['text'], res['statuses'][i]['created_at']])
                next_url = res['metadata']['next_results']
                pattern = r".*max_id=([0-9]*)\&.*"
                ite = re.finditer(pattern, next_url)
                for i in ite:
                    mid = i.group(1)
                    break
            else:
                sys.stdout.write("next is none. finished.")
                break
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.format_exc(sys.exc_info()[2])
        raise
    finally:
        sys.exc_info()