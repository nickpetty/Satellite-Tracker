from Tkinter import *
import Tkinter as tk
import urllib2
from os import listdir


class App:
	def __init__(self):
		self.master = Tk()
		self.master.geometry("800x300")
		self.master.title("Satellite tracker and control")
		#master.configure(background='black')

		self.satGroupSelection = StringVar(self.master)
		self.satGroupSelection.set('Choose List')

		self.satGroupList = OptionMenu(self.master, self.satGroupSelection, '', command=self.updateTLEOptions)
		self.satGroupList.place(x=0,y=0)

		self.chosenSat = StringVar(self.master)
		self.chosenSat.set('Choose Satellite')

		self.TLEOptions = OptionMenu(self.master, self.chosenSat, '')
		self.TLEOptions.place(x=0,y=30)

		self.updateSatGroups()
		self.loadTLEs()	
		self.updateTLEOptions()

		self.loadSatGroup = Button(self.master, text='Load', command=self.updateTLEOptions)
		self.loadSatGroup.place(x=150, y=0)


		# self.tleInfo = StringVar(master)
		# tleInfo.set(str(sats[satSelection.get()]))

		mainloop()

	def updateSatGroups(self):
		options = self.satGroupList["menu"]
		options.delete(0, END)
		self.satGroups = {}
		groups = []
		TLEFiles = listdir('sats')
		for tleFile in TLEFiles:
			self.satGroups[tleFile] = ''
			#command = self.master._setit(self.satGroupSelection, tleFile[:-4], self.updateTLEOptions)
			options.add_command(label=tleFile[:-4], command=tk._setit(self.satGroupSelection, tleFile[:-4]))


	def updateTLEOptions(self):
		if self.satGroupSelection.get()+'.txt' in self.satGroups:
			print 'called'
			options = self.TLEOptions["menu"]
			options.delete(0, END)
			for tleName in self.satGroups[self.satGroupSelection.get()+'.txt']:
				#self.availableTlEs.append(tleName)
				options.add_command(label=tleName, command=tk._setit(self.chosenSat, tleName[:-4]))


	def updateTLE(self):
		for sats in self.satGroups:
			tle = urllib2.urlopen('http://www.celestrak.com/NORAD/elements/' + sats).read()
			file = open('sats/' + sats, 'w+').write(tle)

		self.loadTLEs()


	def loadTLEs(self):
		for group in self.satGroups:
			sats = {}
			tleFile = open('sats/' + group, 'r').readlines() #read in whole file
			tle = []
			for line in tleFile: # Seperate lines into list
				 tle.append(line)

			i = 0
			while (i <= len(tle)) and (i + 3 < len(tle)): # Create dict in dict for each sat : tleData
				sats[tle[i].rstrip()] = {tle[i+1].rstrip():tle[i+2].rstrip()}
				i+=3

			self.satGroups[group] = sats # Add sats dict with sat:tle nested to satGroups


app = App()
