TfL London Underground Line Status Server
==============

This server uses Redis and Flask to develop a system where a user could query the Transport for London London Underground API to get operational information about a particular London Underground line and station (to see whether it is operational or delayed etc.)

The server uses Redis to frequently poll and cache line information to reduce the number of API requests to the Transport for London API. This is done using Cron (scripts in the Cron directory)

Please note, you will need to have your server IP authorised by TfL before you can start making requests against their API.

This server was developed as part of the University of Birmingham Computer Science Degree Final Year Project in 2013 titled 'Intelligent Journey Planning iPhone application for London Underground' by Suhail Patel (sxp013@cs.bham.ac.uk). 