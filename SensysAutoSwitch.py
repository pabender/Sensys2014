# This is an example script for a JMRI "Automat" in Python
# It is based on the AutomatonExample.
#
# It listens to two sensors, running a locomotive back and
# forth between them by changing its direction when a sensor
# detects the engine. 
#
# Author:  Howard Watkins, January 2007.
# Part of the JMRI distribution
#
# The next line is maintained by SVN, please don't change it
# $Revision: 17977 $

import jarray
import jmri

class SensysDemo(jmri.jmrit.automat.AbstractAutomaton) :

	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
		print "Inside init(self)"

		# set up sensor numbers
		# fwdSensor is reached when loco is running forward
		self.fwdSensor = sensors.provideSensor("ZSSPROG:1")
		# define reverse sensors for each track. 
		self.track1RevSensor = sensors.provideSensor("ZSYARD INPUT:1")
		self.track2RevSensor = sensors.provideSensor("ZSYARD INPUT:3")
		self.track3RevSensor = sensors.provideSensor("ZSYARD INPUT:6")
		self.track1UncoupleSensor = sensors.provideSensor("ZSYARD INPUT:0")
		self.track2UncoupleSensor = sensors.provideSensor("ZSYARD INPUT:2")
		self.track3UncoupleSensor = sensors.provideSensor("ZSYARD INPUT:4")
		self.revSensor=self.track1RevSensor
		
		# specify turnouts
		self.turnout1 = turnouts.provideTurnout("ST1")
		self.turnout2 = turnouts.provideTurnout("ST2")
		# set both turnouts to a known state (CLOSED)
		self.turnout1.setState(CLOSED);
		self.waitMsec(2000)          # wait for 2 seconds
		self.turnout2.setState(CLOSED);

		# get loco address. For long address change "False" to "True" 
		# self.throttle = self.getThrottle(710, True)  # short address 14
		self.throttle = self.getThrottle(6338, True)  # short address 14
		
		# Set the address for the "pink" boxcar. 
		self.pinkBoxCar = self.getThrottle(3196, True)  # long address 3196 
		# make sure function 3 is off
     		self.pinkBoxCar.setF3(False)
		# Set the address for the "blue" boxcar. 
		self.blueBoxCar= self.getThrottle(5535, True)  # long address 5535 
		# make sure function 3 is off
     		self.blueBoxCar.setF3(False)
		# Set the address for the "black" boxcar. 
		self.blackBoxCar= self.getThrottle(3, True)  # short address 3 
		# make sure function 3 is off
		self.blackBoxCar.setF3(False)
		
		# get the reporter object
		self.reporter = reporters.provideReporter("FR1")
		self.lastReport = self.reporter.getLastReport()
		
		return

	def handle(self):
		# handle() is called repeatedly until it returns false.
		print "Inside handle(self)"

		# set loco to forward
		print "Set Loco Forward"
		self.throttle.setIsForward(True)
		
		# wait 1 second for layout to catch up, then set speed
		self.waitMsec(1000)                 
		print "Set Speed"
		self.throttle.setSpeedSetting(0.1)
                
                print self.throttle.getSpeedSetting()
                
		# wait for sensor in forward direction to trigger, then stop
		print "Wait for Forward Sensor"
		self.waitSensorActive(self.fwdSensor)
		print "Set Speed Stop"
		self.throttle.setSpeedSetting(0)
		self.throttle.setF0(False)     # turn off headlight
		
		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		print "wait 20 seconds"
		self.waitMsec(20000)          # wait for 20 seconds
		# Decide which turnout to throw based on the current layout state.
		self.lastReport = self.reporter.getLastReport()
		print "Last Reporter report: " 
		print self.lastReport.toString()
		if (self.lastReport.toString() == "WSOR503196" and self.turnout1.getState()==CLOSED and self.turnout2.getState()==CLOSED ):
			print "Switch to track 3"
			self.turnout1.setState(THROWN)
			self.waitMsec(2000)          # wait for 2 seconds
			self.turnout2.setState(CLOSED)
		elif (self.lastReport.toString() == "SLSF15535" and self.turnout1.getState()==CLOSED and self.turnout2.getState()==CLOSED ):
			print "Switch to track 3"
			self.turnout1.setState(THROWN)
			self.waitMsec(2000)          # wait for 2 seconds
			self.turnout2.setState(CLOSED)
		elif (self.lastReport.toString() == "RDG33266" and (self.turnout1.getState()==CLOSED or self.turnout2.getState()==CLOSED) ):
			print "Switch to track 2"
			self.turnout1.setState(THROWN)
			self.waitMsec(2000)          # wait for 2 seconds
			self.turnout2.setState(THROWN)
		else:
			print "Switch to track 1"
			self.turnout1.setState(CLOSED)
			self.waitMsec(2000)          # wait for 2 seconds
			self.turnout2.setState(CLOSED)
		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		print "wait 20 seconds"
		self.waitMsec(20000)          # wait for 20 seconds
		self.throttle.setF0(True)     # turn on headlight
		
		# set direction to reverse, set speed
		print "Set Loco Reverse"
		self.throttle.setIsForward(False)
		self.waitMsec(1000)                 # wait 1 second for network to catch up
		print "Set Speed"
		self.throttle.setSpeedSetting(0.1)

		# wait for sensor in reverse direction to trigger
		if (self.turnout1.getState()==CLOSED):
			print "Wait for Track 1 Reverse Sensor"
			if(self.track1UncoupleSensor.knownState == ACTIVE): 
				self.waitSensorActive(self.track1RevSensor)
			else:
				self.waitSensorActive(self.track1UncoupleSensor)
		elif (self.turnout2.getState()==CLOSED):
			print "Wait for Track 3 Reverse Sensor"
			if(self.track3UncoupleSensor.knownState == ACTIVE): 
				self.waitSensorActive(self.track3RevSensor)
			else:
				self.waitSensorActive(self.track3UncoupleSensor)
			self.waitSensorActive(self.track3RevSensor)
		else:
			print "Wait for Track 2 Reverse Sensor"
			if(self.track2UncoupleSensor.knownState == ACTIVE): 
				self.waitSensorActive(self.track2RevSensor)
			else:
				self.waitSensorActive(self.track2UncoupleSensor)
		print "Set Speed Stop"
		self.throttle.setSpeedSetting(0)
		
		self.throttle.setF0(False)     # turn off headlight
		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		print "wait 20 seconds"
		self.waitMsec(20000)          # wait for 20 seconds
		self.throttle.setF0(True)     # turn on Headlight 
		
		# and continue around again
		print "End of Loop"
		return 1	
		# (requires JMRI to be terminated to stop - caution
		# doing so could leave loco running if not careful)

# end of class definition

# start one of these up
SensysDemo().start()

