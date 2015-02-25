import math
import time
from datetime import datetime, timedelta
from dateutil import tz
import ephem # pip install pyephem
import calendar
import numpy as np


class SatTracker:

	def __init__(self, homeLat, homeLon, homeEv, line1, line2, line3):

		self.degrees_per_radian = 180.0 / math.pi
 
		self.home = ephem.Observer()
		self.home.lat = np.deg2rad(homeLat)
		self.home.lon = np.deg2rad(homeLon)
		self.home.elevation = homeEv # meters

		self.iss = ephem.readtle(line1, line2, line3)

	def utc_to_local(self, utc_dt):
		timestamp = calendar.timegm(utc_dt.timetuple())
		local_dt = datetime.fromtimestamp(timestamp)
		assert utc_dt.resolution >= timedelta(microseconds=1)
		return local_dt.replace(microsecond=utc_dt.microsecond)


	def track(self):
		#print datetime.utcnow()
		self.home.date = datetime.utcnow()
		self.iss.compute(self.home)
		lat = self.iss.sublat * self.degrees_per_radian
		lng = self.iss.sublong * self.degrees_per_radian
		az = self.iss.az * self.degrees_per_radian
		print az
		ev = self.iss.alt * self.degrees_per_radian
		print ev
		return {'az':az, 'ev':ev, 'lat':lat, 'lng':lng}
