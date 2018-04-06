from TwitterAPI import TwitterAPI, TwitterRestPager, TwitterError
import json, time

from secrets import consumer_key, consumer_secret, access_token_key, access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

data = json.load(open('friends.json'))
# json.dump(data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)
data_followers = json.load(open('followers.json'))

main_account = "dam_io"
while True:
    try:
        for account_data in sorted(data_followers[main_account], key=lambda x: x['friends_count']):
            account = account_data["screen_name"]
            if account not in data or account_data['friends_count'] != len(data[account]):
                print('friends/', account, '(', account_data['friends_count'], ')')
                if account_data['protected']:
                    print('-> protected')
                    continue
                data[account] = data.get(account, []) # TODO: complete when rate limit is hit during iteration
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

