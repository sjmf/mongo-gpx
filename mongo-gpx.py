#!/usr/bin/env python
import gpxpy, gpxpy.gpx
from datetime import datetime
from pymongo import MongoClient

# Parse arguments from command line
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--csv", help="Output CSV instead of GPX", action="store_true")
args = parser.parse_args()

# Read TPV packets from Mongo, write to GPX
client = MongoClient()
db = client.car

print( db.gps.count() )
cursor = db.gps.find()

if args.csv:
    with open('out.csv', 'w') as f:
        for document in cursor:
            f.write( str(document['lat']) +','+ str(document['lon']) +','+ str(document['alt']) +'\n')

else:
# Create GPX file using gpxpy
    gpx = gpxpy.gpx.GPX()

# Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

# Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

# Create points:
    for document in cursor:
        gpx_segment.points.append(
            gpxpy.gpx.GPXTrackPoint(
                document['lat'], 
                document['lon'], 
                elevation=document['alt'], 
                time=datetime.strptime(document['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            ))

    with open('out.gpx', 'w') as f:
        f.write( gpx.to_xml() )
