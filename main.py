import time
from rotorControl import AntennaController
from satTracker import SatTracker
import numpy as np


antenna = AntennaController('com1')

# homeLat, homeLon, homeEv, TLELine1, TLELine2, TLELine3
tracker = SatTracker(35.90631, -90.06496, 80, 'ISS (ZARYA)',            
'1 25544U 98067A   15052.82955662  .00014550  00000-0  21887-3 0  9990',
'2 25544 051.6465 300.1701 0005835 032.8359 057.1592 15.55079649930082')

sat = tracker.track()

# Initialize
print 'Moving antenna to position...'
antenna.setAz(round(sat['az'])) # set az from 0 to current az
antenna.setEv(abs(round(sat['ev']))) # set ev form 0 to current ev
time.sleep(1) # give time to get to position form zero
print 'Now tracking'


while True: # begin tracking
	sat = tracker.track()
	antenna.setAz(round(sat['az']))
	antenna.setEv(abs(round(sat['ev'])))
	time.sleep(1)
