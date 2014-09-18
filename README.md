# raven-cosm

A library to connect a Rainforest Automation RAVEn Smart Meter
interface to the weMonitor Rainforest API.  Includes a general
thread-safe message passing framework for publish / subscribe and a
stream-based architecture/

## TODO

### rename the repo

Once upon a time, this repository was for pushing RAVEn data to the
cosm.com API.  It no longer serves that purpose, so it would be
appropriate to rename the repository.

### add documentation

Figure out how Python apps are documented and add appropriate comments
and markups to the source files.  Include a roadmap to the files.

### make the app into a proper daemon

see http://raspberrypi.stackexchange.com/questions/23152/best-practices-for-hardening-an-rpi-for-continuous-remote-monitoring

see http://mmonit.com/monit/

see https://wiki.debian.org/LSBInitScripts

talk to someone at Roku, Sonos, Slim Devices, etc...they would know
about making bulletproof little appliances

for init.d stuff:

see http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html
http://blog.scphillips.com/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

Comprehensive daemonizing of a python script:
https://github.com/nicholasdavidson/pybit
https://pypi.python.org/pypi/python-daemon/
http://www.gavinj.net/2012/06/building-python-daemon-process.html

