# twitter followers network

- [demo dam_io](http://dam.io/twitter-followers-network/dam_io/)
- [demo medialab_ScPo](http://dam.io/twitter-followers-network/medialab_ScPo/)
- [demo anvaka](http://dam.io/twitter-followers-network/anvaka/)
- [demo algoglitch](http://dam.io/twitter-followers-network/algoglitch/)

```
# collect data
mkdir friends
echo "{}" > followers.json
pip install TwitterAPI==2.4.6 twint

add secrets.py with your twitter secrets

python tw.py <twitter_account> # run multiple instances in parrallel to make it faster

python make_friends.py # at the end

# data to graph
npm i graphology graphology-pagerank graphology-communities-louvain graphology-gexf

node rank2.js <twitter_account>
# or
node rank2.js <twitter_account> 1 # mutual follows only

# result in graph.gexf => use gephi to make something pretty
```
