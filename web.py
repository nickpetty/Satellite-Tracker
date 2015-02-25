from flask import Flask, render_template, Response, request, jsonify, Markup
from os import listdir
import simplejson as json
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from gevent import sleep
from satTracker import SatTracker
from rotorControl import dmxAntennaController
import time
gevent.monkey.patch_all()

app = Flask(__name__)

satGroups = {}
name = ''
line1 = ''
line2 = ''

antenna = dmxAntennaController('/dev/tty.usbmodemfd121')
antenna.calibrate()
time.sleep(3)

@app.route('/')
def index():
	loadTLEs()
	#print satGroups
	return render_template('index.html', groups=json.dumps(satGroups))


@app.route('/tle/<group>/<satName>')
def tle(group, satName):
	open('config', 'w').write(group+'\n'+satName)
	return 200


@app.route('/streamSatData')
def sseSatData():
	return Response(tleData(), mimetype='text/event-stream')


def tleData():

	while True:
		sat = open('config', 'r').readlines()
		tle = satGroups[sat[0].rstrip()][sat[1].rstrip()]
		track = SatTracker(35.90631, -90.06496, 80, sat[1].rstrip(), tle[0], tle[1]).track()
		antenna.setCoord(track['az'], abs(track['ev']))
		data = {'lat':round(track['lat'],2), 'lng':round(track['lng'],2), 'az':round(track['az'],2), 'ev':round(track['ev'],2)}	
		yield 'data: %s\n\n' % json.dumps(data)
		gevent.sleep(1)


def updateTLE():
	global satGroups
	for sats in satGroups:
		tle = urllib2.urlopen('http://www.celestrak.com/NORAD/elements/' + sats).read()
		file = open('sats/' + sats, 'w+').write(tle)
	loadTLEs()


def loadTLEs():
	global satGroups

	for tleFile in listdir('sats'):
		satGroups[tleFile[:-4]] = ''

	for group in satGroups:
		sats = {}
		tleFile = open('sats/' + group + '.txt', 'r').readlines() #read in whole file
		tle = []
		for line in tleFile: # Seperate lines into list
			 tle.append(line)

		i = 0
		while (i <= len(tle)) and (i + 3 < len(tle)): # Create dict in dict for each sat : tleData
			sats[tle[i].rstrip()] = [tle[i+1].rstrip(),tle[i+2].rstrip()]
			i+=3

		satGroups[group] = sats # Add sats dict with sat:tle nested to satGroups

updateTLE()

if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=8080, debug=True)
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()




