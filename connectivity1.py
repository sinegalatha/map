import subprocess
import os.path
def install(name):
    subprocess.call(['pip','install',name])
    print("success")
install("folium")
install("mysql-connector-python")

import mysql.connector
import folium
mydb=mysql.connector.connect(user='root', password='Muruga@123',database='accident')
mycursor=mydb.cursor()
f = folium.Figure(width=1000, height=500)
m = folium.Map(location=[10.95771, 78.08095],zoom_start=5,min_zoom = 12,map_type='HYBRID').add_to(f)
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}

# Add custom basemaps
basemaps['Google Maps'].add_to(m)
basemaps['Google Satellite Hybrid'].add_to(m)
from flask import Flask,render_template, render_template_string, request
app = Flask(__name__)
@app.route('/',methods=['GET'])
def hello():
    return render_template('welcome.html')
@app.route('/mymapping',methods=["GET"])
def mymapping():
    mydb = mysql.connector.connect(user='root', password='Muruga@123', database='accident')
    mycursor = mydb.cursor()
    #mycursor.execute("select count(*) from manage")
    p = []
    tbl = "<tr><td>ID</td><td>Name</td><td>Vechicle Type</td><td>Vechicle number</td><td>Date</td><td>Female</td></tr>"
    p.append(tbl)
    #for i in mycursor:
       # acount=i[0]
    mycursor.execute("select * from manage")
    result = mycursor.fetchall()
    for i in result:
        x = i[1]
        y = i[2]
        e=i[0]
        mycursor.execute("""select * from %s""" % (e))
        fg = folium.FeatureGroup(name=i[0])
        result1 = mycursor.fetchall()
        mycursor.execute("""select count(*) from %s""" % (e))
        for n in mycursor:
            acount=n[0]
        p = []
        q = []
        tbq = """table{
            font-family: arial,sans-serif;
            border-collapse:collapse;
            }
            td,th{
            border:1px solid #dddddd;
            text-align:left;
            padding: 8px;
            }
            tr nth-child(even)
            {
            background-color: #dddddd;
            }"""
        q.append(tbq)

        tbl = "<tr><td>Name</td><td>Age</td><td>Type of Vehicle</td><td>Vehicle Number</td><td>Date</td><td>Gender</td></tr>"
        p.append(tbl)

        for row in result1:

            a = "<tr><td>%s</td>" % row[0]
            p.append(a)
            b = "<td>%s</td>" % row[1]
            p.append(b)
            c = "<td>%s</td>" % row[2]
            p.append(c)
            d = "<td>%s</td>" % row[3]
            p.append(d)
            d = "<td>%s</td>" % row[4]
            p.append(d)
            d = "<td>%s</td>" % row[5]
            p.append(d)
        #print(p)
        contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
            <html>
            <head>
            <style>
            table{
            font-family: arial,sans-serif;
            border-collapse:collapse;
            }
            td,th{
            border:1px solid #dddddd;
            text-align:left;
            padding: 8px;
            }
            tr nth-child(even)
            {
            background-color: #dddddd;
            }
            </style>
            <meta content="text/html; charset=ISO-8859-1"
            http-equiv="content-type">
            <title>%s</title>
            </head>
            <body>
            <table>
            %s
            </table>
            </body>
            </html>
            ''' % (e, p)
        #print(contents)
        filename = e + '.html'
        #print(filename)

        def main(contents, filename):
            output = open(filename, "w")
            output.write(contents)
            content = "Accident details count:" + str(acount) + "<br><a href=\"C:\\Users\Sinegalatha\PycharmProjects\map\MADURAI.html\">view</a><br><br>"
            popup = folium.Popup(contents, max_width=500, min_width=200)
            fg.add_child(folium.Marker(location=[x, y], tooltip=e+" "+str(acount), popup=popup,icon=folium.Icon(color="red", icon='car', prefix='fa')))
            m.add_child(fg)
            output.close()

        main(contents, filename)
        #content = "Accident details count:" + str(acount) + "<br><a href=\"C:\\Users\Sinegalatha\PycharmProjects\map\MADURAI.html\">view</a><br><br>"
        #popup = folium.Popup(content, max_width=500, min_width=200)
        #fg.add_child(folium.Marker(location=[x, y], tooltip=acount, popup=popup,icon=folium.Icon(color="red", icon='car', prefix='fa')))
        #m.add_child(fg)
    html_string = m.get_root().render()

    m.save("mymapping1.html")
    return render_template_string(html_string)
if __name__ == '__main__':
    app.run(debug=True)