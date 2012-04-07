#! python
"""
Find the best route that connects all the rental stations in the Boston Hubway 
bike rental network (http://www.thehubway.com/). This is essentially a
travelling salesman problem.

Richard West
r.h.west@gmail.com
"""

from xml.etree.ElementTree import ElementTree
import urllib2
import urllib
import json
import os
import numpy
import time

class Station():
	def __init__(self):
		self.id = 0
	def __repr__(self):
		return "<Station %2d>" % self.id
	def __str__(self):
		return self.lat+','+self.long
	pass


def distancematrix(startplaces,endplaces):
    geo_args = {
    	'origins': startplaces,
    	'destinations': endplaces,
    	'mode': 'bicycling',
    	'sensor': "false",
    	}
    BASE_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json'
    url = BASE_URL + '?' + urllib.urlencode(geo_args)
    result = json.load(urllib2.urlopen(url))
    assert(result['status']!='OVER_QUERY_LIMIT')

    num_stations = len(stations)
    times = numpy.zeros((len(startplaces), len(endplaces)), dtype=numpy.int32) # times in seconds
    distances = numpy.zeros((len(startplaces), len(endplaces)), dtype=numpy.int32) # distances in m
    for i,row in enumerate(result['rows']):
    	for j,element in enumerate(row['elements']):
    	    if element['status']=='ZERO_RESULTS':
    	        print 'ZERO_RESULTS for '  + result['origin_addresses'][i]  + ' to ' + result['destination_addresses'][j]
    	    else:
    		    times[i][j] = element['duration']['value']
    		    distances[i][j] = element['distance']['value']
    return times,distances
        
        
stations_file = urllib2.urlopen('http://thehubway.com/data/stations/bikeStations.xml')

tree = ElementTree()
tree.parse(stations_file)
stations = list()
for s in tree.iter('station'):
	station = Station()
	station.id = int(s.find('id').text)
	station.lat = s.find('lat').text
	station.long = s.find('long').text
	station.name = s.find('name').text
	stations.append(station)


number_of_hackers=2
this_hacker=0 #hacker number 0 of 2
assert this_hacker < number_of_hackers
number_each=int(numpy.ceil(len(stations)/float(number_of_hackers)))

startstations=stations[this_hacker*number_each:(this_hacker+1)*number_each]
endstations=stations
number_of_rowblocks=int(numpy.ceil(number_each/10.0))
number_of_colblocks=int(numpy.ceil(len(stations)/10.0))

for idx_row in xrange(number_of_rowblocks):
    for idx_col in xrange(number_of_colblocks):
        startplaces_ids = '|'.join([str(s.id).rjust(2) for s in stations[this_hacker*number_each:(this_hacker+1)*number_each][idx_row*10:(idx_row+1)*10] ])
        endplaces_ids = '|'.join([str(s.id).rjust(2) for s in stations[(idx_col*10):(idx_col+1)*10]])
        
        startplaces = '|'.join([str(s) for s in stations[this_hacker*number_each:(this_hacker+1)*number_each][idx_row*10:(idx_row+1)*10] ])
        endplaces = '|'.join([str(s) for s in stations[(idx_col*10):(idx_col+1)*10]])
        print 'start ' + startplaces_ids +',  end ' + endplaces_ids
         
        
        distfilename = 'dist_matrix_'+str(this_hacker*number_of_rowblocks+idx_row)+'_'+str(idx_col)+'.numpy'
        timefilename = 'time_matrix_'+str(this_hacker*number_of_rowblocks+idx_row)+'_'+str(idx_col)+'.numpy'
        if os.path.exists(distfilename) and os.path.exists(timefilename):
            print 'skipping ' + distfilename + ' and ' + timefilename
                
        else:
            times,distances = distancematrix(startplaces,endplaces)
            with open(distfilename,'w') as f:
                    distances.tofile(f)
            with open(timefilename,'w') as f:
                    distances.tofile(f)
            print 'writing ' + distfilename + ' and ' + timefilename      
            time.sleep(numpy.random.rand()*2+12)
            



