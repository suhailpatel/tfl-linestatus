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

r = requests.get(tfl_globals.LINE_STATUS_URL)
if r.status_code != 200:
  print "Could not refresh line status feed, got status code %d" % r.status_code
  sys.exit(1)
  
doc = minidom.parseString(r.content)

# Parse the data retrieved from TfL
statuses = {}
line_status = doc.getElementsByTagName('LineStatus')
for line in line_status:
  # Loop through each line and print it's status
  status_details  = line.attributes['StatusDetails'].value.strip()
  line_name       = line.getElementsByTagName('Line')[0].attributes['Name'].value.strip()
  
  if not tfl_globals.LINE_NAME_MAP.has_key(line_name):
    continue
  
  line_code       = tfl_globals.LINE_NAME_MAP[line_name]
  status          = line.getElementsByTagName('Status')[0]
  status_id       = status.attributes['ID'].value.strip()
  status_desc     = status.attributes['Description'].value.strip()
  
  statuses[line_code] = {
    'status_id': status_id,
    'status_desc': status_desc,
    'status_details': status_details,
    'line': line_name
  }

# Update our data on the server side
redis_conn.conn.set('line_status', statuses)
redis_conn.conn.set('line_status:updated', str(time.time()))