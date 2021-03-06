from flask import Flask, render_template, request, json
import os
import urllib.request
from jinja2 import ext
from datetime import datetime

app = Flask(__name__)

with urllib.request.urlopen("https://apis.is/petrol") as url:
    data = json.loads(url.read().decode())

#app.jinja_env.add_extension(ext.do)

def format_time(gogn):
    return datetime.strptime(gogn, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d. %m. %Y Kl. %H:%M')
#app.jinja_env.filters['format_time'] = format_time

bensinstodvar = []
myndir = {'Atlantsolía': 'atlantsolia.png', 'Costco Iceland': 'costco.png', 'Dælan':'daelan.png',
          'N1':'n1.png', 'ÓB':'ob.png', 'Olís':'olis.png', 'Orkan':'orkan.png'}

bensin95  = []
diesel = []

stadur_bensin95 = []
stadsetning_bensin95 = []
nafnBensin = []

stadur_diesel = []
stadsetning_diesel = []
nafnDiesel = []



@app.route('/')
def home():
    for item in data['results']:
        bensin95.append(item['bensin95'])
        diesel.append(item['diesel'])
        if item['company'] not in bensinstodvar:
            bensinstodvar.append(item['company'])
            
    for i in data['results']:
        if min(diesel) == i['diesel']:
            stadur_diesel = i['company']
            nafnDiesel = i['name']          
        if min(bensin95) == i['bensin95']:
            stadur_bensin95 = i['company']
            nafnBensin = i['name']
    
    date = data['timestampApis']
    timi = format_time(date)

    min_bensin_stadur = min(bensin95), stadur_bensin95, nafnBensin
    min_diesel_stadur = min(diesel), stadur_diesel, nafnDiesel
    
    return render_template('index.html', timi=timi, data=data, bensinstodvar=bensinstodvar, mynd=myndir, min_diesel_stadur=min_diesel_stadur, min_bensin_stadur=min_bensin_stadur)

@app.route('/stadur/<stod>/')
def soluadill(stod):
    stadsetningar = []
    for item in data['results']:
        if item['company'] == stod:
            if item['name'] not in stadsetningar:
                stadsetningar.append(item['name'])
    return render_template('soluadili.html', stod=stod, stadsetningar=stadsetningar)

@app.route('/stadur/<stod>/<bensinstod>')
def bensinstod(stod, bensinstod):
    for item in data['results']:
        if item['name'] == bensinstod:
            verd_bensin = item['bensin95']
            verd_diesel = item['diesel']
            lat = item['geo']['lat']
            lon = item['geo']['lon']
    return render_template('bensinstod.html', lon=lon, lat=lat, verd_diesel = verd_diesel, verd_bensin = verd_bensin, bensinstod=bensinstod, stod=stod)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404villa.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
