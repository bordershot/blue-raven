#/bin/bash
#
sleep 10 &
echo sleep pid = $!
pkill sleep
echo exiting...

