#!/usr/bin/env python
#-*- coding: utf-8 -*-

import binascii

class NMEA0183():

    def __init__(self):
        self.data = ''
        self.data_gps = {'lat': '0.0',
                         'lon': '0.0',
                         'speed': float(0.0),
                         'track': float(0.0),
                         'utc': '0.0',
                         'status': 'A'}

    def process(self):
        if self.data[4:7] == 'RMC':
            information = self.data.split(',')
            if information[2] != 'A':
                print('NO DATA!')
                return False
            self.data_gps['utc'] = self.gps_nmea2utc(information[1])
            self.data_gps['lat'] = information[3][0:2] + '.' + str(float(information[3][2:9]) * 100 / 60)\
                .replace('.', '')
            self.data_gps['lon'] = information[5][0:3] + '.' + str(float(information[5][3:10]) * 100 / 60)\
                .replace('.', '')
            self.data_gps['speed'] = float(information[7]) * 1.15078
            if information[4] == 'S': self.data_gps['lat'] = '-' + self.data_gps['lat']
            if information[6] == 'W': self.data_gps['lon'] = '-' + self.data_gps['lon']

    def makechecksum(self,data):
        '''Calculates a checksum from a NMEA sentence.

        Keyword arguments:
        data -- the NMEA sentence to create

        '''
        csum = 0
        i = 0
        # Remove ! or $ and *xx in the sentence
        data = data[1:data.rfind('*')]
        while (i < len(data)):
            input = binascii.b2a_hex(data[i])
            input = int(input,16)
            #xor
            csum = csum ^ input
            i += 1
        return csum

    def checksum(self,data):
        '''Initiates variables and opens serial connection.

        Keyword arguments:
        data -- the NMEA sentence to check

        '''
        try:
            # Create an integer of the two characters after the *, to the right
            supplied_csum = int(data[data.rfind('*')+1:data.rfind('*')+3], 16)
        except:
            return ''
        # Create the checksum
        csum = self.makechecksum(data)
        # Compare and return
        if csum == supplied_csum:
            return True
        else:
            return False

    def gps_nmea2utc(self, the_data):
        '''Converts NMEA utc format to more standardized format.'''
        time = the_data[1][0:2] + ':' + the_data[1][2:4] + ':' + the_data[1][4:6]
        date = '20' + the_data[9][4:6] + '-' + the_data[9][2:4] + '-' + the_data[9][0:2]
        return date + 'T' + time + 'Z'