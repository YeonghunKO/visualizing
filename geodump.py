import sqlite3
import json
import codecs

conn = sqlite3.connect("C:\\Bitnami\\wampstack-7.4.6-1\\apache2\\htdocs\\geoload.sqlite")
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('C:\\Bitnami\\wampstack-7.4.6-1\\apache2\\htdocs\where.js', 'w', "utf-8")#create javascript file.
fhand.write("myData = [\n")#start writing array and data into the javascript file
count = 0
for row in cur :
    data = str(row[1].decode()) #row[1] is geocode from locations table of SQLite.
    try: js = json.loads(str(data))#convert the location into string and parse it.
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue #you can group the couple of statments.

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")##Get rid of single dot to make it neat and clean.
    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output) ## Write wanted infos(lat,lng,formatted_address) into the javascript file.
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")#And you can see the whole results of this beautiful code by checking the javascript file which is called where.js
