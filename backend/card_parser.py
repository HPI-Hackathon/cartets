# Client thread started for each player
import urllib2
import json
import random
import re

# \d+(?=\s?[pP][sS])

def main(long,lat):
    response = urllib2.urlopen('http://m.mobile.de/svc/s/?ll=' + str(long) + ',' + str(lat) + '&s=Car&psz=100&sb=doc')
    data = json.load(response)['items']
    gameCars = validation(data)
    return gameCars


# ^[0-9\.]+

def validation(list):
    resList = []
    while len(resList) <= 20:
        #for elem in dict:
        elem = random.choice(list)

        if 'images' in elem and 'pw' in elem['attr'] and 'ml' in elem['attr'] and 'csmpt' in elem['attr']:
            image = elem['images'][0].get('uri')+'_8.jpg'
            title = elem['title']
            price = elem['price']['grs']['amount']
            power = re.search('\d+(?=(\s|\xA0)?[pP][sS])', elem['attr']['pw']).group(0)
            dist = re.search('^[0-9\.]+', elem['attr']['ml']).group(0)
            first = '.'.join(reversed(elem['attr']['fr'].split('/')))
            location = '{:f},{:f}'.format(elem['contact']['latLong']['lat'], elem['contact']['latLong']['lon'])
            url = elem['url']
            try:
                consumption = re.search('^[^0-9]*\d+\,\d+', elem['attr']['csmpt']).group(0).replace(',','.')
            except Exception, e:
                continue
            current = {'title': title, 'image': image, 'price': price, 'registration': first, 'mileage': dist, 'power': power, 'consumption': consumption, 'location': location, 'url': url}
            final = json.dumps(current)
            resList.append(final)
    return resList


if __name__ == '__main__':
    main()
