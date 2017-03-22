from subject import *
from observer import *
import xml.etree.ElementTree as ET
import sys
import socket
import time

server='192.168.37.25'
port=2003
proto='udp'

dataToGather = { 'SummationDelivered', 'Demand', 'SummationReceived', 'CurrentUsage' }

class upload_to_graphite(Subject, Observer):

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)

    # support for observer
    def getValue(self, xmltree, stringValue):
        '''Returns a single float value for the SummationDelivered from a Summation response from RAVEn'''
        # Get the Current Summation (Meter Reading)
        #  fReading = float(int(xmltree.find(stringValue).text,16))
        tempReading = xmltree.find(stringValue).text
        # logger.info("tempReading: " + tempReading)
        negativeNum = "0x7"
        while len(negativeNum) < len(tempReading):
            negativeNum += "f"
        negativeNum = float(int(negativeNum,16))
        fReading = float(int(tempReading,16))
        if fReading > negativeNum:
            fReading -= (2 * negativeNum)
        fResult = self.calculateRAVEnNumber(xmltree, fReading)
        return self.formatRAVEnDigits(xmltree, fResult)

    def calculateRAVEnNumber(self, xmltree, value):
        '''Calculates a float value from RAVEn using Multiplier and Divisor in XML response'''
        # Get calculation parameters from XML - Multiplier, Divisor
        fDivisor = float(int(xmltree.find('Divisor').text,16))
        fMultiplier = float(int(xmltree.find('Multiplier').text,16))
        if (fMultiplier > 0 and fDivisor > 0):
            fResult = float( (value * fMultiplier) / fDivisor)
        elif (fMultiplier > 0):
            fResult = float(value * fMultiplier)
        else: # (Divisor > 0) or anything else
            fResult = float(value / fDivisor)
        return fResult

    def formatRAVEnDigits(self, xmltree, value):
        '''Formats a float value according to DigitsRight, DigitsLeft and SuppressLeadingZero settings from RAVEn XML response'''
        # Get formatting parameters from XML - DigitsRight, DigitsLeft
        iDigitsRight = int(xmltree.find('DigitsRight').text,16)
        iDigitsLeft = int(xmltree.find('DigitsLeft').text,16)
        sResult = ("{:0%d.%df}" % (iDigitsLeft+iDigitsRight+1,iDigitsRight)).format(value)
        # Suppress Leading Zeros if specified in XML
        if xmltree.find('SuppressLeadingZero').text == 'Y':
            while sResult[0] == '0':
                sResult = sResult[1:]
        return sResult

    def update(self, message):
        timestamp = int(time.time())
        tcp_output = ""

        xmltree = ET.fromstring(message)
        for k in dataToGather:
            if xmltree.find(k) is not None:
                tcp_output += "power." + str(k) + " " + self.getValue(xmltree, k) + " " + str(timestamp) + "\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((server, port))   # tuple of (servername, port)
            s.sendall(tcp_output.encode('ascii'))
            s.close()
        except:
            sys.stderr.write('ERROR: Could not write to Graphite ' +
                             str(sys.exc_info()[0]))
            pass

        self.notify(message)
