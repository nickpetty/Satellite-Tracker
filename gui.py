from Tkinter import *
import urllib2

master = Tk()
master.geometry("800x300")
master.title("Satellite tracker and control")
#master.configure(background='black')

satGroups = {'stations.txt', 'weather.txt', 'noaa.txt'}

def updateTLE():
	global satGroups
	for sats in satGroups:
		tle = urllib2.urlopen('http://www.celestrak.com/NORAD/elements/' + sats).read()
		file = open('sats/' + sats, 'w+').write(tle)

def loadTLE():
	sats = {}
	tleFile = open('sats/stations.txt', 'r').readlines()
	tle = []
	for line in tleFile:
		 tle.append(line)

	i = 0
	while (i <= len(tle)) and (i + 3 < len(tle)):
		sats[tle[i].rstrip()] = {tle[i+1].rstrip():tle[i+2].rstrip()}
		i+=3

	return sats

satOptions = []
sats = loadTLE()

for sat in sats:
	satOptions.append(sat)

satSelection = StringVar(master)
satSelection.set(satOptions[0])

satList = apply(OptionMenu, (master, satSelection) + tuple(satOptions))
satList.pack()

tleInfo = StringVar(master)
tleInfo.set(str(sats[satSelection.get()]))

tleLabel = Label(master, text=tleInfo.get())
tleLabel.pack()




master.mainloop()
