import time
from rotorControl import dmxAntennaController
from satTracker import SatTracker
import numpy as np


#antenna = dmxAntennaController('/dev/tty.usbmodemfd121')

# homeLat, homeLon, homeEv, TLELine1, TLELine2, TLELine3
tracker = SatTracker(35.90631, -90.06496, 80, 'ISS (ZARYA)',            
'1 21263U 91032A   15052.57758029  .00000061  00000-0  43966-4 0  9994',
'2 21263  98.6413  81.2372 0013161 227.6087 245.2602 14.25733062236098')

sat = tracker.track()

# Initialize
#antenna.calibrate()
print 'Positioning...'
time.sleep(3)
sat = tracker.track()
#antenna.setCoord(sat['lat'], abs(sat['lng']))

# print 'Moving antenna to position...'
# antenna.setAz(round(sat['az'])) # set az from 0 to current az
# antenna.setEv(abs(round(sat['ev']))) # set ev form 0 to current ev
# time.sleep(1) # give time to get to position form zero
# print 'Now tracking'


while True: # begin tracking
	sat = tracker.track()
	#antenna.setCoord(sat['az'], abs(sat['ev']))
	#antenna.setAz(round(sat['az']))
	#antenna.setEv(abs(round(sat['ev'])))
	time.sleep(1)
