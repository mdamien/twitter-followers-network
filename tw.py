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


followers = data_followers[main_account]
random.shuffle(followers)

while True:
    for account_data in followers:
        account = account_data["screen_name"]

        print('friends/', account, ' (', account_data['friends_count'], ')', sep='')
        if account_data['protected']:
            print('-> protected')
            continue
        count = 0

        data_account = []

        if os.path.exists('friends/%s.json' % account):
            continue

        try:
            import os
            cmd = 'twint -u %s --following --json -o %s.json > /dev/null' % (account, account)
            print(cmd)
            os.system(cmd)
            with open(account + '.json') as f:
                for line in f:
                    item = json.loads(line)
                    data_account.append({
                        'screen_name': item['username']
                    })
            os.system('rm %s.json' % account)
            break
        except FileNotFoundError:
            pass
        time.sleep(1)

        print(' ->', len(data_account))
        json.dump(data_account, open('friends/%s.json' % account, 'w'), indent=2, sort_keys=True, ensure_ascii=False)

