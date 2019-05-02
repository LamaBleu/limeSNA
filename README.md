# limeSNA ported to ADALM-PLUTO
This is a Scalar Network Analyzer program initialy written for the LimeSDR mini by github user nepeee (https://github.com/nepeee/limeSNA).  
I replaced the SoapySDR layer by pow tool, and added Pluto TXgain and RXgain parameters to the webpage.  
Sweep time is not optimal and can be improved : approx. 1 hop/s 

Youtube : https://www.youtube.com/watch?v=yh-9a1fkgFA

Dependencies
- pow tool : https://github.com/LamaBleu/plutoscripts/tree/master/pluto_power  
           : you will need to compile pow tool.
- numpy (pip)
- flask (pip)
- flask_socketio (pip)
- webbrowser (pip)
- gevent (pip)
- gevent-websocket (pip)

How to use:

Install all the dependencies and run the code from a terminal with the following command:

python sna.py

After the radio is ready to use, the program starts a new web browser with the UI. Press the run button to start the frequeny sweep. For relative("calibrated") measurements wait a full sweep and then press the "Set relative" button.

