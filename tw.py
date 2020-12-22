from TwitterAPI import TwitterAPI, TwitterRestPager, TwitterError
import json, time, sys, glob

import random
import os.path

from secrets import consumer_key, consumer_secret, access_token_key, access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

data_followers = json.load(open('followers.json'))

main_account = sys.argv[1]

while True:
    try:
        if main_account not in data_followers or len(data_followers[main_account]) == 2000:
            print('followers/', main_account)
            r = TwitterRestPager(api, 'followers/list', {'screen_name': main_account, 'count': 200})
            data_followers[main_account] = []
            for item in r.get_iterator(wait=60):
                data_followers[main_account].append(item)
                if len(data_followers[main_account]) % 200 == 0:
                    print('....', len(data_followers[main_account]))
            print(' ->', len(data_followers[main_account]))
            json.dump(data_followers, open('followers.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break
    except TwitterError.TwitterRequestError as e:
        print(e)
        time.sleep(60)
    except KeyboardInterrupt as e:
        print('saviiinggg...')
        json.dump(data_followers, open('followers.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break


data = json.load(open('friends.json'))

while True:
    try:
        for account_data in sorted(data_followers[main_account], key=lambda x: x['followers_count']):
            account = account_data["screen_name"]
            if account not in data:
                print('friends/', account)
                if account_data['protected']:
                    print('-> protected')
                    continue
                data[account] = []
                count = 0

                r = TwitterRestPager(api, 'friends/list', {'screen_name': account, 'count': 200})
                for item in r.get_iterator():
                    data[account].append(item)
                print(' ->', len(data[account]))
                json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break
    except TwitterError.TwitterRequestError as e:
        print(e)
        time.sleep(2*60) # 15 min between resets of API limit
    except KeyboardInterrupt as e:
        print('saviiinggg...')
        json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break