// TODO global mutual follows ?

const Graph = require('graphology');
const pagerank = require('graphology-pagerank');

const graph = new Graph();

console.log('loading followers')
var followers = require("./algoglitch/followers.json");
console.log('loading friends')
var friends = require("./algoglitch/friends.json");
var account = process.argv[2];
console.log('processing', account);

add = (x, type) => graph.addNode(x.screen_name, {
	label: x.screen_name,
	type: type,
	url:'https://twitter.com/'+x.screen_name,
	followers: x.followers_count,
	friends_count: x.friends_count,
	location: x.location,
	name: x.name,
	status: x.status ? x.status.text : '',
	statuses_count: x.statuses_count,
	favourites_count: x.favourites_count,
	description: x.description.replace(/[^\x20-\x7E]+/g, ""),
	profile_img: x.profile_image_url_https,
})

console.log('add followers')
followers[account].forEach(x =>
	add(x, 'follow_you')
);

console.log('add friends')
Object.keys(friends).forEach(key => {0
	if (key != account) friends[key].forEach(x => {
		if (x.screen_name == account) return;
		if (!graph.hasNode(key)) {
			return;
		}
		if (!graph.hasNode(x.screen_name)) {
			return; // uncomment to have the
			add(x, 'followed_by_your_followers')
		}
		if (!graph.hasEdge(key, x.screen_name)) {
			graph.addEdge(key, x.screen_name);
		} else {
			// WTF
			console.log('duplicate edge !!', key, x.screen_name)
		}
	})
});

console.log('Number of nodes', graph.order);
console.log('Number of edges', graph.size);

// console.log('Nodes', graph.nodes());


// TODO http://labs.polsys.net/tools/rankflow/

// To compute pagerank and return the score per node:
const p = pagerank(graph); // TODO/ LOG() IT ? TO BE MORE LINEAR
var arr = Object.keys(p).map(k => [p[k], k])
arr.sort((a,b) => a[0] - b[0])
arr.slice(arr.length-30,arr.length).forEach(x => console.log(x, graph.inDegree(x[1])))
/*
console.log(p['migueldeicaza'], graph.inDegree('migueldeicaza'), graph.outDegree('migueldeicaza'))
console.log(p['peter_vermeulen'], graph.inDegree('peter_vermeulen'), graph.outDegree('peter_vermeulen'))

// graph.edges('peter_vermeulen').forEach(x => console.log(x))
console.log(graph._nodes.get('peter_vermeulen').out)
/*
g.forEachLinkedNode('hello', function(linkedNode, link){
    console.log("Connected node: ", linkedNode.id, linkedNode.data);
    console.dir(link); // link object itself
});
*/

var louvain = require('graphology-communities-louvain');
louvain.assign(graph);


pagerank.assign(graph);
var gexf = require('graphology-gexf/browser');
var gexfString = gexf.write(graph);
var fs = require('fs');
fs.writeFile("graph.gexf", gexfString, function(err) {
    if(err) {
        return console.log(err);
    }
});
