import glob, json

all_data = {}

for file in glob.glob('friends/*.json'):
	data = json.load(open(file))
	username = file.split('/')[1].split('.')[0]
	all_data[username] = data

json.dump(all_data, open('friends.json', 'w'), indent=2, sort_keys=True, ensure_ascii=False)

