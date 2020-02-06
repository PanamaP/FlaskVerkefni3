from flask import Flask, render_template, request, json
import os
import urllib.request
import config 
from config import api_key

app = Flask(__name__)

with urllib.request.urlopen("https://apis.is/petrol") as url:
    data = json.loads(url.read().decode())

bensinstodvar = []
myndir = {'Atlantsolía': 'atlantsolia.png', 'Costco Iceland': 'costco.png', 'Dælan':'daelan.png',
          'N1':'n1.png', 'ÓB':'ob.png', 'Olís':'olis.png', 'Orkan':'orkan.png'}

bensin95  = []
diesel = []

stadur_bensin95 = []
stadsetning_bensin95 = []

stadur_diesel = []
stadsetning_diesel = []



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
        if min(bensin95) == i['bensin95']:
            stadur_bensin95 = i['company']
    min_bensin_stadur = min(bensin95), stadur_bensin95
    min_diesel_stadur = min(diesel), stadur_diesel
    
    return render_template('index.html', data=data, bensinstodvar=bensinstodvar, mynd=myndir, min_diesel_stadur=min_diesel_stadur, min_bensin_stadur=min_bensin_stadur)

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
            verd_bensin_discount = item['bensin95_discount']
            verd_diesel = item['diesel']
            verd_diesel_discount = item['diesel_discount']
            lat = item['geo']['lat']
            lon = item['geo']['lon']
    return render_template('bensinstod.html', lon=lon, lat=lat,verd_diesel_discount = verd_diesel_discount, verd_diesel = verd_diesel, verd_bensin_discount = verd_bensin_discount, verd_bensin = verd_bensin, bensinstod=bensinstod, stod=stod, api_key=api_key)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404villa.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
