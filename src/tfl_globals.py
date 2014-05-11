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

LINES = ['B', 'C', 'D', 'H', 'J', 'M', 'N', 'P', 'V', 'W']

LINE_NAME_MAP = {
  'Bakerloo': 'B',
  'Central': 'C',
  'Circle': 'Ci',
  'District': 'D',
  'DLR': 'DLR',
  'Hammersmith and City': 'H',
  'Jubilee': 'J',
  'Metropolitan': 'M',
  'Northern': 'N',
  'Overground': 'O',
  'Piccadilly': 'P',
  'Victoria': 'V',
  'Waterloo and City': 'W'
}

LINE_STATUS_URL = "http://cloud.tfl.gov.uk/TrackerNet/LineStatus"
TIME_STATUS_URL = "http://cloud.tfl.gov.uk/TrackerNet/predictionsummary"