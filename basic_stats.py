import json

DATA = json.load(open('followers.json'))

account = 'dam_io'
print(account, 'followers with the most followers')
data = DATA[account]
data.sort(key=lambda x: -x['followers_count'])
for x in data[:20]:
	print(x['followers_count'], x['name'], x['screen_name'])

print()
print(account, 'followers with the most friends')
data = DATA[account]
data.sort(key=lambda x: -x['friends_count'])
for x in data[:40]:
	print(x['friends_count'], x['name'], x['screen_name'])

"""
print()
print()
print('who are', account, 'followers top following followers ?')
data = [f for k, followers in json.load(open('data.json')).items() if k != account for f in followers]
data.sort(key=lambda x: -x['followers_count'])
for x in data[:20]:
	print(x['followers_count'], x['name'], x['screen_name'])
"""

print()
print('who are', account, 'followers also following in', account, 'followers ?')
from collections import Counter
account_followers = {x['screen_name'] for x in DATA[account]}
following_of_followers = []
for k, followers in DATA.items():
	if k != account:
		for f in followers:
			if f['screen_name'] in account_followers:
				following_of_followers.append(f['screen_name'])
c = Counter(following_of_followers)
for x, n in c.most_common(10):
	print(x, n)


print()
print('who are', account, 'followers also following ?')
from collections import Counter
following_of_followers = []
for k, followers in DATA.items():
	if k != account:
		for f in followers:
			following_of_followers.append(f['screen_name'])
c = Counter(following_of_followers)
for x, n in c.most_common(20):
	print(x, n)
