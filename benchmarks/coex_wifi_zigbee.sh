#/bin/bash
#
# Test for coexistence issues between a colocated WiFi USB dongle and a ZigBee dongle.
#
# PREREQUISITES:
#
# * A Raspberry Pi
# * A Rainforest Automation RAVEN ZigBee Smart Meter HAN device
# * A WiFi adapter, configured to run in the 2.4GHz band (channels 1-13).
#
# The test works as follows:
# 
# It first runs a baseline test, where it reads raw ZigBee Smart
# Energy Profile packets via the Rainforest RAVEN.  The packets are
# written to a temp file.
#
# It runs the same test, but this time running a flood ping on the 
# WiFi adaptor.  At the end of the test, it prints the ping statistics.
#

PROJECT_ROOT=$(cd `dirname "${BASH_SOURCE[0]}"`/.. && pwd)

TEST_DURATION=600
PYTHON=/usr/bin/python
LIBRARY_PATH=$PROJECT_ROOT/lib
SCRIPTS_PATH=$PROJECT_ROOT/scripts
BASE_FILE=/tmp/cwz0.xml
COEX_FILE=/tmp/cwz1.xml
ROUTER_ADDRESS=192.168.1.1


echo ==== Baseline test...
rm $BASE_FILE
PYTHONPATH=$LIBRARY_PATH $PYTHON $SCRIPTS_PATH/file_write_script.py $BASE_FILE > /dev/null &
sleep $TEST_DURATION
pkill python
wc $BASE_FILE

echo === Coexistence test...
rm $COEX_FILE
PYTHONPATH=$LIBRARY_PATH $PYTHON $SCRIPTS_PATH/file_write_script.py $COEX_FILE > /dev/null &
ping -f -q $ROUTER_ADDRESS &
sleep $TEST_DURATION
pkill -INT ping
pkill python
wc $COEX_FILE

