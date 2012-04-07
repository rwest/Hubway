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

class Station():
	def __init__(self):
		self.id = 0
	def __repr__(self):
		return "<Station %2d>" % self.id
	def __str__(self):
		return self.lat+','+self.long
	pass

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
	
stations = stations[:10] # just deal with first 10 for now, as there's a cap on calls to google API


places = '|'.join([str(s) for s in stations])
geo_args = {
	'origins': places,
	'destinations': places,
	'mode': 'bicycling',
	'sensor': "false",
	}
BASE_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json'
url = BASE_URL + '?' + urllib.urlencode(geo_args)
result = json.load(urllib2.urlopen(url))
assert(result['status']!='OVER_QUERY_LIMIT')

num_stations = len(stations)
times = numpy.zeros((num_stations, num_stations), dtype=numpy.int32) # times in seconds
distances = numpy.zeros((num_stations, num_stations), dtype=numpy.int32) # distances in m
for i,row in enumerate(result['rows']):
	for j,element in enumerate(row['elements']):
		times[i][j] = element['duration']['value']
		distances[i][j] = element['distance']['value']

times

