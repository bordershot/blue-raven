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

### incorporate syslog

The current version prints (lots of stuff) to stdout and capture it
with nohup.  It would be more useful to emit status, error and
diagnostic messages using the syslog facility.  (And that will set the
state for sending syslog output to a remote logging service.)

### better testing

The basic lib modules are tested, but we need better testing at the
edges (e.g. reading from USB, posting to web service, issuing calls to
syslog).  There is a good introduction to writing mocks in Python in

  http://www.toptal.com/python/an-introduction-to-mocking-in-python#.

### Create sandboxed development environment on OS X platform

For testing (notably, when I don't have direct access to the RPi), I
need a sandboxed environment on the Mac that approximates the RPi
python environment.  At a minimum, I need a "more modern" python (3.4
or greater) and the requests package.  Probably more.
