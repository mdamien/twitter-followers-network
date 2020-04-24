# FAIRE LE DIAGRAM RANK CHANGE (RANK FLOW)

from TwitterAPI import TwitterAPI, TwitterRestPager, TwitterError
import json, time, sys

from secrets import consumer_key, consumer_secret, access_token_key, access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

data = json.load(open('friends.json'))
# json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
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

while True:
    try:
        for account_data in sorted(data_followers[main_account], key=lambda x: x['friends_count']):
            account = account_data["screen_name"]
            if account not in data or account_data['friends_count'] > len(data[account]):
                print('friends/', account, ' (', account_data['friends_count'], ')', sep='')
                if account_data['protected']:
                    print('-> protected')
                    continue
                data[account] = data.get(account, []) # TODO: complete when rate limit is hit during iteration
                count = 0

                while True:
                    try:
                        import os
                        cmd = 'rm following.json;twint -u %s --following --json -o following.json > /dev/null' % account
                        print(cmd)
                        os.system(cmd)
                        with open('following.json') as f:
                            for line in f:
                                item = json.loads(line)
                                data[account].append({
                                    'screen_name': item['username']
                                })
                        break
                    except FileNotFoundError:
                        pass

                """
                r = TwitterRestPager(api, 'friends/list', {'screen_name': account, 'count': 200})
                for item in r.get_iterator(wait=60):
                    data[account].append(item)
                    if len(data[account]) % 200 == 0:
                        print('....', len(data[account]))
                """
                print(' ->', len(data[account]))
                json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break
    except TwitterError.TwitterRequestError as e:
        print(e)
        time.sleep(60)
    except KeyboardInterrupt as e:
        print('saviiinggg...')
        json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
        break

