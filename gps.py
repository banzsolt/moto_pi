#!/usr/bin/python
# get lines of text from serial port, save them to a file

from __future__ import print_function
import serial, io
import nmea
import requests

addr  = '/dev/ttyUSB0'  # serial port to read data from
baud  = 4800            # baud rate for serial port
fname = 'gps-log.dat'   # log file to save data in
fmode = 'a'             # log file mode = append
tracking_website = 'https://moto-tracker.herokuapp.com/rootes/new_entry'

with serial.Serial(addr,baud) as pt, open(fname,fmode) as outf:
    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
        encoding='ascii', errors='ignore', newline='\r',line_buffering=True)
    spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
    reader = nmea.NMEA0183()
    while (1):
        x = spb.readline()  # read one line of text from serial port
        #print (x,end='')    # echo line of text on-screen
        outf.write(x)       # write line of text to file
        outf.flush()        # make sure it actually gets written out
        reader.data = x
        reader.process()
        headers = {'device_token': 'D16tL9tgBz2mKgcHullQB3kquwoRFtY4N0tLx1ksqRpZBSvZGEFgclrY6SrM'}
        data = {'latitude': reader.data_gps['lat'],
                'longitude': reader.data_gps['lon'],
                'speed': reader.data_gps['speed'],
                'time': reader.data_gps['utc'], }
        r = requests.post(tracking_website, headers=headers, data=data)