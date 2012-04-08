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
	def prettystring(self):
		return "%s at %s"%(self.name, str(self))
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

    
    times = numpy.zeros((len(result['origin_addresses']), len(result['destination_addresses'])), dtype=numpy.int32) # times in seconds
    distances = numpy.zeros((len(result['origin_addresses']), len(result['destination_addresses'])), dtype=numpy.int32) # distances in m
    for i,row in enumerate(result['rows']):
    	for j,element in enumerate(row['elements']):
    	    if element['status']=='ZERO_RESULTS':
    	        print 'ZERO_RESULTS for '  + result['origin_addresses'][i]  + ' to ' + result['destination_addresses'][j]
    	        times[i][j]=-1
    	        distances[i][j]=-1
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

##################### Change These ####################### 
number_of_hackers=2     # This partitions the problem
this_hacker=0           # hacker number 0 of 2
debug=2       #debug is a limit for testing, make it very big for a full run
data_dir = 'data'
os.path.exists(data_dir) or os.mkdir(data_dir)

assert this_hacker < number_of_hackers
number_each=int(numpy.ceil(len(stations)/float(number_of_hackers)))
startstations=stations[this_hacker*number_each:(this_hacker+1)*number_each]
endstations=stations

number_of_rowblocks=min(debug,int(numpy.ceil(number_each/10.0)))
number_of_colblocks=min(debug,int(numpy.ceil(len(stations)/10.0)))

for idx_row in xrange(number_of_rowblocks):
    for idx_col in xrange(number_of_colblocks):
        startplaces_ids = '|'.join([str(s.id).rjust(2) for s in stations[this_hacker*number_each:(this_hacker+1)*number_each][idx_row*10:(idx_row+1)*10] ])
        endplaces_ids = '|'.join([str(s.id).rjust(2) for s in stations[(idx_col*10):(idx_col+1)*10]])
        
        startplaces = '|'.join([str(s) for s in stations[this_hacker*number_each:(this_hacker+1)*number_each][idx_row*10:(idx_row+1)*10] ])
        endplaces = '|'.join([str(s) for s in stations[(idx_col*10):(idx_col+1)*10]])
        print 'start ' + startplaces_ids +',  end ' + endplaces_ids
         
        
        distfilename = os.path.join(data_dir,'dist_matrix_'+str(this_hacker*number_of_rowblocks+idx_row)+'_'+str(idx_col)+'.txt')
        timefilename = os.path.join(data_dir,'time_matrix_'+str(this_hacker*number_of_rowblocks+idx_row)+'_'+str(idx_col)+'.txt')
        if os.path.exists(distfilename) and os.path.exists(timefilename):
            print 'skipping ' + distfilename + ' and ' + timefilename
        else:
            times,distances = distancematrix(startplaces,endplaces)
            #with open(distfilename,'w') as f:
            #        distances.tofile(f)
            #with open(timefilename,'w') as f:
            #        distances.tofile(f)
            numpy.savetxt(distfilename,distances)
            numpy.savetxt(timefilename,times)
            print 'writing ' + distfilename + ' and ' + timefilename      
            time.sleep(numpy.random.rand()*2+12)
            
from matplotlib import pyplot as plt

times=numpy.zeros((len(stations),len(stations)),dtype=numpy.int32)
time_matrix_list=[a for a in os.listdir(data_dir) if a.startswith('time_matrix') and a.endswith('.txt')]
for time_matrix in time_matrix_list:
    row,col=time_matrix.split('.')[0].split('_')[2:4]
    row=int(row)
    col=int(col)
    timesblock=numpy.genfromtxt(os.path.join(data_dir,time_matrix))
    print row,col
    times[row*10:(row+1)*10,col*10:(col+1)*10]=timesblock[0:10,0:10]

plt.spy(times)
plt.show()

plt.spy(times==-1) 
plt.show()
# the shape of this is discouraging: did we screw up somewhere?

# get the rows with more than one negative one
inaccessible_stations = set(((times==-1).sum(1)>1).nonzero()[0])
# add the columns with more than one negative one
inaccessible_stations = inaccessible_stations.union(((times==-1).sum(0)>1).nonzero()[0])
print "Difficulty accessing these stations, so removing them:"
for s in inaccessible_stations:
	print stations[s].prettystring()
keepers = range(len(times))
for s in inaccessible_stations:
	keepers.remove(s)
pruned_times = times[keepers][:,keepers]

pruned_stations = [stations[i] for i in range(len(stations)) if i in keepers]
plt.spy(pruned_times==-1)

