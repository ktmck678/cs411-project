import sys
import json
import requests
import re
from datetime import datetime
'''
cs411 Program
Usage python scheduler.py <time span> <calendars> <output>

'''
###
#
# Retrieve Schedule
#
###

def getEvents(ecps):
	events = []
	for ecp in ecps:
		calendar = ecp['calendar']
		r = requests.get('https://www.googleapis.com/calendar/v3/calendars/%s/events?key=AIzaSyAp4guGasaQV75hpYBNhI3kMT4SyZf_QnI' % calendar)
		es = r.json()['items']
		for e in es:
			rule = []
			if 'recurrence' in e:
				if 'DAILY' in str(e['recurrence']):
					rule = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']
				elif 'BYDAY' in str(e['recurrence']):
					r = re.match('.*BYDAY=(.*)$',e['recurrence'][0])
					if r != None:
						groups = r.groups()
						if len(groups) > 0:
							rule = groups[0].split(',')
			dt = e['start']['dateTime']
			start = datetime.strptime(dt[:len(dt) - 6], '%Y-%m-%dT%H:%M:%S').hour
			dt = e['end']['dateTime']
			end = datetime.strptime(dt[:len(dt) - 6], '%Y-%m-%dT%H:%M:%S').hour
			events += [
			{'rule': rule, 'start': start, 'end': end, 'email': ecp['email']}
			]
	return events

###
#
# JSON to Schedule
#
###

def eventsToWeek(events):
	ss = []
	for dow in ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']:
		schedule = {
		'dow': dow,
		'schedules': {},
		'streches': []
		}
		ss += [schedule]

	for e in events:
		for dow in e['rule']:
			for s in ss:
				if s['dow'] == dow:
					if e['email'] in s['schedules']:
						s['schedules'][e['email']] += [e]
					else:
						s['schedules'][e['email']] = [e]
	return ss





###
#
# Map
# 
###
def free_time(schedule):
	return [hour for hour in range(0, 24) if reduce (lambda x, y: x and y, [not e['start'] <= hour < e['end'] for e in schedule])]

def free_time_stretches(email, schedule, stretch):
	stretches = []
	for i, hour in enumerate(schedule[:len(schedule) - stretch]):
		if range(hour, hour + stretch) == schedule[i:i + stretch]:
			stretches += [((hour, hour + stretch), email)]
	return stretches

def mapper(schedules, span):
	retVal = []
	for schedule in schedules:
		retVal += free_time_stretches(schedule['email'], free_time(schedule['schedule']), span)
	return retVal

###
#
# Reduce
#
###

def Map(f, R):
	return [t for (k,v) in R for t in f(k,v)]
    
def Reduce(f, R):
	keys = {k for (k,v) in R}
	return [f(k1, [v for (k2,v) in R if k1 == k2]) for k1 in keys]

def reducer(ss):
	def aux(k, vs):
		start, end = k
		return {'start': start, 'end': end, 'emails': vs}
	return Reduce(aux, ss)

def dowToDOW(dow):
	DOWS = {
	'SU':'Sunday',
	'MO':'Monday',
	'TU':'Tuesday',
	'WE':'Wednesday',
	'TH':'Thursday',
	'FR':'Friday',
	'SA':'Saturday'
	}
	if dow in DOWS:
		return DOWS[dow]
	else:
		return 'Sunday'

def main():
	span = int(sys.argv[1])
	in_f = open(sys.argv[2])
	ecps = json.load(in_f)
	in_f.close()
	es = getEvents(ecps)
	ss = eventsToWeek(es)
	#print ss[0]

	for s in ss:
		schedules = []
		for k in s['schedules']:
			schedules += [{'email': k, 'schedule': s['schedules'][k]}]
		iv = mapper(schedules, span)
		s['stretches'] = sorted(reducer(iv), key = lambda x: len(x['emails']) * 100 + abs(15 - x['start']))

	#print [(s['dow'], s['stretches'][0]) for s in ss]
	fv = [{'dayOfWeek': dowToDOW(s['dow']), 'start': '%02d:00' % s['stretches'][0]['start'], 'end': '%02d:00' % s['stretches'][0]['end']} for s in ss if len(s['stretches']) > 0]

	if len(sys.argv) == 4:
		out_f = open(sys.argv[3], 'w')
		out_f.write(json.dumps(fv))
		out_f.close()
	else:
		print json.dumps(fv)
		sys.stdout.flush()
	'''
	

	iv = mapper(schedules, span)
	fv = sorted(reducer(iv), key = lambda x: len(x['emails']))

	out_f = open(sys.argv[3], 'w')
	out_f.write(json.dumps(fv))
	out_f.close()
	'''

'''
def main():
	span = int(sys.argv[1])
	schedules = json.load(sys.stdin)
	iv = mapper(schedules, span)
	fv = sorted(reducer(iv), key = lambda x: len(x['emails']))
	print json.dumps(fv)
	sys.stdout.flush()
'''

if __name__ == "__main__":
	main()




