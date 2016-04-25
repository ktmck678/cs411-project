var express = require('express');
var bodyParser = require('body-parser');

var app = express();
app.use(bodyParser.json());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.post('/api/meetingTime', bodyParser.json(), function (req, res, next) {
	//check body
	if (!('timeSpan' in req.body) or !('calendars' in req.body)) {
		res.json({'error':'invalid or malformed request'})
	}
	res.json({'times':[
		{
			'id': 1,
			'datetime':'2016-04-26T17:00:00',
			'dayOfWeek':'Tuesday'
		}
	]})
});

app.post('/api/archiveValue', function (req, res, next) {
	if (!('id' in req.body)) {
		res.json({'error':'invalid or malformed request'})
	}
	res.json({'times':[
		{
			'datetime':'2016-04-26T17:00:00',
			'dayOfWeek':'Tuesday'
		}
	]})
})

app.listen(3000);
console.log("Server running on port 3000");