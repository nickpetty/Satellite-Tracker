import serial # pip install pyserial
import time

class AntennaController:

	currentAZ = 0
	currentEV = 0
	
	def __init__(self, comPort):
		#self.rotator = serial.Serial(comPort, baudrate=115200)
		pass

	def setAz(self, targetAZ): # Degree 0-360
		self.currentAZ
		targetAZ = round(targetAZ)

		if targetAZ < self.currentAZ:
			degreeDiff = self.currentAZ - targetAZ # If targetAZ (280) is < currentAZ (340) subtract targetAZ from currentAZ (60) rotate ccw 60 steps.
			dirc = 'ccw'
			steps = int(round(degreeDiff/1.41)) # convert degree difference to step for 400step/rev motor
			print 'rotate ccw for ' + str(steps) + ' steps from ' + str(int(self.currentAZ)) + ' to ' + str(int(targetAZ))
			# self.rotator.write(AB'+str(steps)) # 'A' - Azimuth, 'B' - ccw
			self.currentAZ = targetAZ


		if targetAZ > self.currentAZ:
			degreeDiff = targetAZ - self.currentAZ # If targetAZ (340) is > currentAZ (280) subtract currentAZ from targetAZ (60) rotate cw 60 steps.
			dirc = 'cw'
			steps = int(round(degreeDiff/1.41)) # convert degree difference to step for 400step/rev motor
			print 'rotate cw for ' + str(steps) + ' steps from ' + str(int(self.currentAZ)) + ' to ' + str(int(targetAZ))
			# self.rotator.write('AF'+str(steps)) # 'A' - Azimuth, 'F' - cw
			self.currentAZ = targetAZ

		# if targetAZ == currentAZ: do nothing.
	  

	def setEv(self, targetEV): # Degree 0-90
		self.currentEV
		targetEV = round(targetEV)

		if targetEV in range(0,90): # Assuming there is only 90 degrees of elevation from the current Azimuth
			if targetEV < self.currentEV:
				degreeDiff = self.currentEV - targetEV
				dirc = 'cw'
				steps = int(round(degreeDiff/1.41))
				print 'lower (cw) for ' + str(steps) + ' steps from ' + str(int(self.currentEV)) + ' to ' + str(int(targetEV))
				# self.rotator.write('EB'+str(steps)) # 'E' - elevation, 'B' - ccw
				self.currentEV = targetEV

			if targetEV > self.currentEV:
				degreeDiff = targetEV - self.currentEV
				dirc = 'ccw'
				steps = int(round(degreeDiff/1.41))
				print 'raise (ccw) for ' + str(steps) + ' steps from ' + str(int(self.currentEV)) + ' to ' + str(int(targetEV))
				# self.rotator.write('EF'+str(steps)) # 'E' - elevation, 'F' - cw
				self.currentEV = targetEV

class dmxAntennaController:

	def __init__(self, comPort):
		self.rotator = serial.Serial(comPort, baudrate=115200)
		time.sleep(2)

	def setCoord(self, targetAZ, targetEV):
		dmxAz = int(round(targetAZ/2.1))
		dmxEv = ''

		if int(round(targetEV)) in range(0,90):
			dmxEv = int(round((targetEV/2.1)+50))

		self.rotator.write(str(dmxAz) + ',0,' + str(dmxEv) + '~')

		print 'AZ: ' + str(int(round(targetAZ))) + ' EV: ' + str(int(round(targetEV))) + ' - moverAz: ' + str(dmxAz) + ' moverEv: ' + str(dmxEv) 

	def calibrate(self):
		print 'Calibrating...'
		self.rotator.write('0,0,50~')
		print 'DMX - AZ: ' + str(0) + ' EV: ' + str(50)
		time.sleep(3)








