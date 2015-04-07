# Client thread started for each player
import urllib2
import json
import random


def run(long,lat):
    response = urllib2.urlopen('http://m.mobile.de/svc/s/?ll=' + long + ',' + lat + '&s=Car&psz=100&sb=doc')
    data = json.load(response)['items']
    gameCars = validation(data)
    print gameCars
    return gameCars


def validation(list):
    resList = []
    while len(resList) <= 20:
        #for elem in dict:
        elem = random.choice(list)

        if 'images' in elem and 'pw' in elem['attr'] and 'ml' in elem['attr']:
            if 'csmpt' in elem['attr']:
                image = elem['images'][0].get('uri')+'_8.jpg'
                title = elem['title']
                price = elem['price']['grs']['amount']
                power = elem['attr']['pw']
                dist = elem['attr']['ml']
                first = elem['attr']['fr']
                consumption = elem['attr']['csmpt']
                current = {'title': title, 'image': image, 'price': price, 'registration': first, 'mileage': dist, 'power': power, 'consumption': consumption}
                final = json.dumps(current)
                resList.append(final)
    return resList



