import time
from rotorControl import AntennaController
from satTracker import SatTracker

antenna = AntennaController('com1')

# homeLat, homeLon, homeEv, TLELine1, TLELine2, TLELine3
tracker = SatTracker(35.0500, -89.9848, 86, 'ISS (ZARYA)',            
'1 25544U 98067A   15051.80472707  .00012522  00000-0  18963-3 0  9999',
'2 25544  51.6466 305.2870 0005813  27.4514  81.5032 15.55046614929922')

sat = tracker.track()

# Initialize
print 'Moving antenna to position...'
antenna.setAz(round(sat['az'])) # set az from 0 to current az
antenna.setEv(abs(round(sat['ev']))) # set ev form 0 to current ev
time.sleep(20) # give time to get to position form zero
print 'Now tracking'


while True: # begin tracking
	sat = tracker.track()
	antenna.setAz(round(sat['az']))
	antenna.setEv(abs(round(sat['ev'])))
	time.sleep(1)
