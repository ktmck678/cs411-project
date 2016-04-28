var express = require('express');
var bodyParser = require('body-parser');
var uuid = require('node-uuid').v4;
var jsonfile = require('jsonfile')
var AWS = require('aws-sdk'); 

AWS.config.update({region: 'us-east-1'})
var ddb = new AWS.DynamoDB()
var dc = new AWS.DynamoDB.DocumentClient()
var table = 'requests'

var app = express();
app.use(bodyParser.json());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.post('/api/meetingTime', bodyParser.json(), function (req, res, next) {
	//check body
	if (!('timeSpan' in req.body) || !('calendars' in req.body)) {
		res.json({'error':'invalid or malformed request'})
	}
	id = uuid()
	file = '/tmp/' + id + '.txt'
	jsonfile.writeFile(file, req.body.calendars, function(err) {});
	var python = require('child_process').spawn('python', ['scheduler.py', req.body.timeSpan, file])
	var output = "";
	python.stdout.on('data', function(data){ output += data });
	python.on('close', function(code){
		res.json({
			id: id,
			times: JSON.parse(output)
		});
		dc.put({
			TableName:table,
			Item: {
				id: id,
				times: JSON.parse(output)
			}
		}, function(err, data){
			if (err) {
				console.log(err)
			}
		})
	});
});

app.post('/api/archiveValue', function (req, res, next) {
	if (!('id' in req.body)) {
		res.json({'error':'invalid or malformed request'})
	}
	dc.get({
		TableName: table,
		Key:{id: req.body.id}
	}, function(err, data) {
		if (err){
			res.json({'error': err})
		} else {
			res.json(data.Item)
		}
	})
})

app.listen(3000);
console.log("Server running on port 3000");