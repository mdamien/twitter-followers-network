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

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.get("https://twitter.com")
input("login and then type enter:")

while True:
    for account_data in followers:
        account = account_data["screen_name"]

        print('friends/', account, ' (', account_data['friends_count'], ')', sep='')
        if account_data['protected']:
            print('-> protected')
            continue

        if os.path.exists('friends/%s.json' % account):
            continue

        followers = set()

        driver.get("https://twitter.com/" + account + '/following')

        time.sleep(5)

        prev_len = -1
        while len(followers) > prev_len:
            prev_len = len(followers)

            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            for span in soup.select('span'):
                text = span.text.split(' ')[0]
                if text.startswith('@'):
                    text = text.replace('@', '')
                    if text != account and text != 'dam_io':
                        followers.add(text)
            driver.execute_script("window.scrollTo(0, 100000)")
            time.sleep(1)

        data_account = []
        for follower in followers:
            data_account.append({
                'screen_name': follower,
            })

        print(' ->', len(data_account))
        json.dump(data_account, open('friends/%s.json' % account, 'w'), indent=2, sort_keys=True, ensure_ascii=False)

