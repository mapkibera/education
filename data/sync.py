#/usr/bin/python
import urllib, urllib2
import base64
import csv
import os

north = -1.3000
south = -1.3232
east = 36.8079
west = 36.7663

def sync():
  url = 'http://overpass-api.de/api/interpreter'
  values = dict(data='<osm-script><osm-script output="json" timeout="25"><union><query type="node"><has-kv k="amenity" v="school"/><bbox-query e="36.8079" n="-1.3000" s="-1.3232" w="36.7663"/></query></union><print mode="body"/><recurse type="down"/><print mode="skeleton" order="quadtile"/></osm-script></osm-script>')  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  rsp = urllib2.urlopen(req)
  print rsp.read()

def url2file(url,file_name):
  req = urllib2.Request(url)
  rsp = urllib2.urlopen(req)
  myFile = open(file_name, 'w')
  myFile.write(rsp.read())
  myFile.close()

def kenyaopendata():
  #https://www.opendata.go.ke/Education/Kenya-Secondary-Schools-2007/i6vz-a543
  url2file('https://www.opendata.go.ke/api/views/i6vz-a543/rows.csv?accessType=DOWNLOAD','kenya-secondary-schools.csv')
  #https://www.opendata.go.ke/Education/Kenya-Primary-Schools-2007/p452-xb7c
  url2file('https://www.opendata.go.ke/api/views/p452-xb7c/rows.csv?accessType=DOWNLOAD','kenya-primary-schools.csv')

def filter_data(input_file,output_file,division_column,location_column,write_id):
  reader = csv.DictReader(open(input_file))
  writer = csv.DictWriter(open(output_file,'w'),['official_name','lat','lon'])
  header = dict()
  header['official_name'] = 'official_name'
  header['lat'] = 'lat'
  header['lon'] = 'lon'
  writer.writerow(header)
  for row in reader:
    [lat,lon] = row[location_column].replace('(','').replace(')','').split(',')
    if row[division_column] == 'KIBERA' or ((float(lat) <= north and float(lat) >= south) and (float(lon) <= east and float(lon) >= west)):
      out_row = dict()
      out_row['official_name'] = row[write_id]
      out_row['lat'] = lat
      out_row['lon'] = lon
      writer.writerow(out_row)

def filter_kenyaopendata():
  filter_data('kenya-primary-schools.csv','kibera-primary-schools.csv','Division','Geolocation','Name of School')
  filter_data('kenya-secondary-schools.csv','kibera-secondary-schools.csv','Division','Location 1','Name of School') #Code??

def convert2geojson():
  os.system("ogr2ogr -f GeoJSON kibera-primary-schools.geojson kibera-primary-schools.vrt")
  os.system("ogr2ogr -f GeoJSON kibera-secondary-schools.geojson kibera-secondary-schools.vrt")

kenyaopendata()
filter_kenyaopendata()
convert2geojson()
