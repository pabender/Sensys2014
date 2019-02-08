This repository contains JMRI control panels and scripts used to control a small RFID test layout.  The layout is configured as an IngleNook siding switching puzle. More information about the layout can be found at

http://nscaleintermodal.com/layout/RFIDTestLayout/

Of interest to JMRI users is how this repository shows an example of using several features.

The layout makes extensive use of XBee devices.  Sensors are connected directly to XBee devices for position feedback.  The XBee devices also provide a connection to an SPROG, which is used to power the trains and control the turnouts.  A ID Innovations ID-20 RFID reader is connected to an XBee and is used in JMRi as a standalone reader.

The panel includes Reporter Icons for 3 reporters.  One reporter is a physical reporter that reports the RFID tags on the main track.  The other two reporters are internal reporters.  The script [ReporterTrackContents.py](https://github.com/pabender/Sensys2014/blob/master/ReporterTrackContents.py) makes use of the switch positions and the CollectingReporter interface available though the internal reporters to keep track of what the last car on the track is. In other words, the reporter always shows the next car available to be pulled from the track.

Also of interest is the [SensysAutoSwitch.py](https://github.com/pabender/Sensys2014/blob/master/SensysAutoSwitch.py) script, which automatically switches cars.  The current version makes a decision as to what track a car should be on based on the RFID tag information read only.
