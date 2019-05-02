from __future__ import print_function
import time
import threading
from flask import Flask, request
from flask_socketio import SocketIO
import webbrowser
import signal
import sys

from SingleToneSweeper import SingleToneSweeper

class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        print('\nYou pressed Ctrl+C - please wait...\n\n')
        self.SIGINT = True
        sys.exit(2)


handler = SIGINT_handler()
signal.signal(signal.SIGINT, handler.signal_handler)


class SNA:
    RUN_MODE_OFF = 0
    RUN_MODE_ON = 1
    RUN_MODE_UPDATE_CONFIG = 2

    thread = None
    socketio = None

    sweeper = None
    snaRunMode = RUN_MODE_OFF
    snaSampleRate = 5e6
    snaStartFreq = 100e6
    snaEndFreq = 110e6
    snaNumSteps = 5
    snarxGain = 60
    snatxGain = -10

    def __init__(self):
        app = Flask(__name__, static_url_path='/static')
        self.socketio = SocketIO(app, async_mode='gevent')

        thread = threading.Thread(target=self.snaThread)
        thread.start()

        @app.route('/')
        def root():
            return app.send_static_file('index.html')

        @self.socketio.on('connect')
        def connect():
            self.socketio.emit('config', {
                'sampleRate': self.snaSampleRate,
                'startFreq': self.snaStartFreq,
                'endFreq': self.snaEndFreq,
                'numSteps': self.snaNumSteps,
                'runMode': self.snaRunMode,
                'rxGain': self.snarxGain,
                'txGain': self.snatxGain
            })

        @self.socketio.on('config')
        def handle_json(json):
            self.snaSampleRate = int(json['sampleRate'])
            self.snaStartFreq = int(json['startFreq'])
            self.snaEndFreq = int(json['endFreq'])
            self.snaNumSteps = int(json['numSteps'])
            self.snaRunMode = int(json['runMode'])
            self.snarxGain = int(json['rxGain'])
            self.snatxGain = int(json['txGain'])

            if ((self.snaRunMode!=self.RUN_MODE_ON) and (self.sweeper is not None)):
                self.sweeper.abortSweep()

        self.socketio.run(app, port=55555)


    def sweepStart(self, startFreq, freqStep, stepCnt):
        self.socketio.emit('sweepStart', {
            'freqMin': startFreq,
            'freqStep': freqStep,
            'stepCnt': stepCnt
        })

    def sweepResult(self, index, pwr):
        self.socketio.emit('data', {
            'x': index,
            'y': pwr
        })

    def snaThread(self):
#args can be user defined or from the enumeration result
#	args = dict(driver="plutosdr",uri="ip:pluto.local")

        self.sweeper = SingleToneSweeper(self.snaSampleRate, 20, 20, self)
        webbrowser.open("http://127.0.0.1:55555", new=1)

        while True:
            if handler.SIGINT:
				break
            if (self.snaRunMode==self.RUN_MODE_OFF):
                time.sleep(0.1)
                continue
            elif (self.snaRunMode==self.RUN_MODE_UPDATE_CONFIG):
                self.snaRunMode = self.RUN_MODE_ON
          
            start = time.time()

            self.sweeper.setSampleRate(self.snaSampleRate)
            self.sweeper.sweep(self.snaStartFreq, self.snaEndFreq, self.snaNumSteps, self.snarxGain, self.snatxGain)

            end = time.time()

            print("sweep time : %4.2f sec." % (end - start))

if __name__ == '__main__':
    SNA()
