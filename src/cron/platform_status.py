# TFL Line Status Server written in Flask and Redis
# Part of the Final Year Project by Suhail Patel
# at the University of Birmingham Computer Science 2013
# 
# Copyright 2013 Suhail Patel/University of Birmingham
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import path

import sys
sys.path.insert(0, path.join(path.dirname(__file__), '../'))

import redis, redis_conn
import tfl_globals
import requests, time
from xml.dom import minidom

# Parse the data retrieved from TfL
for line in tfl_globals.LINES:
  url = "%s/%s" % (tfl_globals.TIME_STATUS_URL, line)
  r = requests.get(url)
  doc = minidom.parseString(r.content)

  if r.status_code != 200:
    print "Could not refresh line feed for line %s, got status code %d" % (line, r.status_code)
    continue
  
  stations = doc.getElementsByTagName('S')
  
  # Loop through all the stations in the list
  for station in stations:
    code        = station.attributes['Code'].value.strip() 
    platforms   = station.getElementsByTagName('P')
    
    # Now go through all the platforms within the station
    platform_data = []
    for platform in platforms:
      platform_name  = platform.attributes['N'].value.strip()
      times          = platform.getElementsByTagName('T')
      
      # Each platform has a bunch of times, get them
      train_times = []
      for timed in times:
        destination = timed.attributes['DE'].value.strip()
        time_to_platform = timed.attributes['C'].value.strip()
        train_times.append({'destination': destination, 'time': time_to_platform})
      
      platform_data.append({'name': platform_name, 'times': train_times})    
    
    redis_conn.conn.set("%s:%s" % (code, line), platform_data)
    
    # Update our data on the server side
    redis_conn.conn.set(("%s:updated" % (line)), str(time.time()))
