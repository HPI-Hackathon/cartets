import urllib2
import json
import random
import re

# \d+(?=\s?[pP][sS])
# ^[0-9\.]+


def main(long, lat, card_list):
    url = 'http://m.mobile.de/svc/s/?ll=' + str(long) + ',' + str(lat) + '&s=Car&psz=100&sb=doc'
    response = urllib2.urlopen(url)
    data = json.load(response)['items']
    return generate_list(data, card_list)


def generate_list(list, card_list):
    res_list = []
    while len(res_list) <= 10:
        elem = random.choice(list)
        if elem['id'] in card_list:
            continue

        item = validate_entry(elem, card_list)
        if item:
            res_list.append(item)
    return res_list


def validate_entry(elem, card_list):
    attr_keys = ['pw', 'ml', 'csmpt']
    if 'images' in elem and all(key in elem['attr'] for key in attr_keys):
        try:
            image = elem['images'][0].get('uri')+'_8.jpg'
            title = elem['title']
            price = elem['price']['grs']['amount']
            power = re.search('\d+(?=(\s|\xA0)?[pP][sS])', elem['attr']['pw']).group(0)
            dist = re.search('^[0-9\.]+', elem['attr']['ml']).group(0)
            first = '.'.join(reversed(elem['attr']['fr'].split('/')))
            location = '{:f},{:f}'.format(elem['contact']['latLong']['lat'], elem['contact']['latLong']['lon'])
            url = elem['url']
            consumption = re.search('\d+\,\d+', elem['attr']['csmpt']).group(0).replace(',','.')

        except:
            return

        card_list.append(elem['id'])
        return json.dumps({'title': title,
                           'image': image,
                           'price': price,
                           'registration': first,
                           'mileage': dist,
                           'power': power,
                           'consumption': consumption,
                           'location': location,
                           'url': url})


if __name__ == '__main__':
    main()
