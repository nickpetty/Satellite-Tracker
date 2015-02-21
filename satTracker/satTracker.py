import math
import time
from datetime import datetime
import ephem # pip install pyephem

class SatTracker:

	def __init__(self, homeLat, homeLon, homeEv, line1, line2, line3):

		self.degrees_per_radian = 180.0 / math.pi
 
		self.home = ephem.Observer()
		self.home.lat = homeLat
		self.home.lon = homeLon
		self.home.elevation = homeEv # meters

		self.iss = ephem.readtle(line1, line2, line3)

	def track(self):
		self.home.date = datetime.utcnow()
		self.iss.compute(self.home)
		az = self.iss.az * self.degrees_per_radian
		#print az
		ev = self.iss.alt * self.degrees_per_radian
		#print ev
		return {'az':az, 'ev':ev}
