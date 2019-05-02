from __future__ import print_function
import os
import math
import time
import numpy as np
from socket import *


class SingleToneSweeper:
	sampleRate = None
	bandWidth = None
	aborted = False
	events = None

	def __init__(self, sampleRate, rxGain, txGain, events):

		self.events = events
		args = dict(driver="plutosdr")
		self.rxGain = 60
		self.setSampleRate(sampleRate)
		self.pwr = 0

	def setSampleRate(self, sampleRate):
		sampleRate = float(sampleRate)

		if (self.sampleRate==sampleRate):
			return

		self.sampleRate = sampleRate
		self.bandWidth = sampleRate


	def abortSweep(self):
		self.aborted = True

	def sweep(self, snaStartFreq, snaEndFreq, snaNumSteps, snarxGain, snatxGain):
		self.aborted = False
		numSteps = int(math.ceil(snaNumSteps / 2))
		txNCOStep = int(round(self.bandWidth / 2 / numSteps))
		txNCOOffset = int(round(txNCOStep / 2))
		txRfFreq = snaStartFreq + txNCOStep*numSteps - txNCOOffset
		self.snarxGain = snarxGain
		self.snatxGain = snatxGain
		self.events.sweepStart(snaStartFreq, txNCOStep, math.floor((snaEndFreq-snaStartFreq) / txNCOStep) + 1)
		print("RXgain :", snarxGain, " -- TXgain :", snatxGain)
		self.plutotx_init(snatxGain)
		n = 0
		brk = False
		while (True):



			for i in range(-1*numSteps, numSteps):

				txNCOFreq = txNCOOffset + txNCOStep*i
				freq = int(txRfFreq + txNCOFreq)
				self.freq = int(freq)
#				print(freq)


#
#		RX : get signal level	
#
				self.plutotx(freq)
				self.pwr = self.plutopower(freq)
				print(n+1, freq, self.pwr)
				self.events.sweepResult(n, float(self.pwr))

				if ((txRfFreq + txNCOFreq >= snaEndFreq) or (self.aborted)):
					brk = True
					print("sweep end or stop")
					time.sleep(0.5)
					break

				n += 1


			if (brk):
				break

			txRfFreq += self.bandWidth
		print("plutotx stop")
		# Pluto : stop bist mode
		os.system("/usr/bin/iio_attr -u ip:pluto.local -D  9361-phy bist_tone \"0 0 0 0\" 2>/dev/null\n")

			
	def plutopower(self, freq):

		cmd = "./pow -l %s -g %s -f %s" %(freq, self.snarxGain, int(self.sampleRate/1000000))
#		print(cmd)
		pow = os.popen(cmd).read()
#		test : pow = os.popen('./pow -l 430600000 -g 40 -f 3').read()

		level = pow.split()
#		print(level)
		self.pwr = repr(float(level[1]))
#		print(self.pwr)
#   	print repr(level[0]), repr(float(level[1]))
		return self.pwr

	def plutotx_init(self, snatxGain):
		print("plutotx_init")
		setpower = "/usr/bin/iio_attr -a -q -c -o ad9361-phy voltage0 hardwaregain %s 1>/dev/null\n" % snatxGain
		os.system(setpower)

		os.system("/usr/bin/iio_attr -a -q -c -o ad9361-phy voltage0 sampling_frequency 1600000 1>/dev/null\n")
		os.system("/usr/bin/iio_attr -a -q -D ad9361-phy bist_prbs 0 1>/dev/null\n")
		os.system("/usr/bin/iio_attr -a -q -D ad9361-phy bist_tone \"1 1 0 0\" 1>/dev/null\n")

	def plutotx(self, freq):
		freqTX = freq - 100000
#		print("plutoTX  -->", freqTX)
		cmd = "/usr/bin/iio_attr -u ip:pluto.local -q -c ad9361-phy TX_LO frequency %s 1>/dev/null\n" % freqTX
#		print(cmd)
		os.system(cmd)
		time.sleep(0.2)

			
