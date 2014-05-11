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
import ast

from flask import Flask
from flask import abort
from flask import jsonify

app = Flask(__name__)

# Default route is not implemented so give an error
@app.route("/")
def hello():
  return jsonify({'error': "No method specified"}), 501

@app.route('/status')
def status():
  # Get the data from Redis
  data = redis_conn.conn.get("line_status")
  updated = redis_conn.conn.get('line_status:updated')
  
  # If we can't get the data we need, abort and return a 404 not found with an 
  # error message
  if data == None or updated == None:
    return jsonify({'error': "Could not load line status data from server"}), 404
  else:
    data = ast.literal_eval(data)
  
  # Otherwise return a JSON version of our data
  return jsonify({'data': data, 'updated': updated}), 200
  
@app.route('/times/<station>/<line>')
def times(station, line):
  # Make sure the key combination exists first
  key = "%s:%s" % (station, line)
  if not redis_conn.conn.exists(key):
    return jsonify({'error': "Data for station/line combination does not exist"}), 404
  
  data = redis_conn.conn.get(key)
  updated = redis_conn.conn.get("%s:updated" % line)
  
  # If we can't get the data we need, abort
  if data == None or updated == None:
    return jsonify({'error': "Could not load data for station/line combination from server"}), 404
  else:
    data = ast.literal_eval(data)
  
  return jsonify({'station': station, 'line': line, 'data': data, 'updated': updated}), 200

if __name__ == "__main__":
  app.run(debug=True)
