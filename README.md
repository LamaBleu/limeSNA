# limeSNA ported to ADALM-PLUTO
This is a Scalar Network Analyzer program initialy written for the LimeSDR mini by github user nepeee (https://github.com/nepeee/limeSNA).  
I replaced the SoapySDR layer by pow tool, and added Pluto TXgain and RXgain controls to the webpage.  
Sweep time is not optimal and can be improved : approx. 1 hop/s 

Youtube : https://www.youtube.com/watch?v=yh-9a1fkgFA

Dependencies  

- pow tool : you will need to compile pow tool.  
  build pow tool :  
           
      gcc -std=gnu99 -g -o pow pow.c -liio -lm -Wall -Wextra
      
   Test :  
   
      ./pow -l 430600000 -g 40 -f 3   
 
   result : 430600000 2.49 95.75   
   units  : freq (Hz), signal (dB) computed by pow, RSSI (dB) returned by pluto through IIO   
            
- numpy (pip)  
- flask (pip)  
- flask_socketio (pip)  
- webbrowser (pip)  
- gevent (pip)  
- gevent-websocket (pip)
- libiio

Quick setup :  

    cd ~  
    git clone https://github.com/LamaBleu/limeSNA  
    cd limeSNA  
    git checkout plutosdr  
    gcc -std=gnu99 -g -o pow pow.c -liio -lm -Wall -Wextra  



How to use:

Install all the dependencies and run the code from a terminal with the following command:  

    python sna.py

After the radio is ready to use, the program starts a new web browser with the UI ( http://127.0.0.1:55555 ). Press the run button to start the frequeny sweep.  
For relative("calibrated") measurements wait a full sweep and then press the "Set relative" button.

