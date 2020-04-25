# twitter followers network

```
# collect data
mkdir friends
echo "{}" > followers.json
pip install TwitterAPI==2.4.6 twint

add secrets.py with your twitter secrets

python tw.py <twitter_account> # run multiple instances in parrallel to make it faster

python make_friends.json # at the end

# data to graph
npm i graphology graphology-pagerank graphology-communities-louvain graphology-gexf

node rank2.js <twitter_account>
# or
node rank2.js <twitter_account> 1 # mutual follows only

# result in graph.gexf => use gephi to make something pretty
```