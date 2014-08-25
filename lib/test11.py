"""Capture raw RAVEn output into a file.

SYNOPSIS:

   test11 filename [npackets]

"""
import sys
import usbio
import stopper
import file_writer
import echo

filename = sys.argv[1]
npackets = int(sys.argv[2]) if len(sys.argv) >= 3 else 50

print("filename = " + filename + " npackets = " + str(npackets))

usb = usbio.USBIO()
# Instruct stopper to send a stop() message to usb after npackets
stp = stopper.Stopper(usb, npackets)
fwr = file_writer.FileWriter(filename)
ech = echo.Echo()

usb.attach(fwr).attach(stp).attach(ech)
usb.start()
usb.thread.join()

