# Client thread started for each player
import urllib2
import json

def main():
    #response = urllib2.urlopen('http://m.mobile.de/svc/s/?ll=' + ll)
    response = urllib2.urlopen('http://m.mobile.de/svc/s/?ll=52.516,13.376')
    data = json.load(response)['items']
    gameCars = validation(data)
    print gameCars

def validation(dict):
    resList = []
    while len(resList) <= 20:
        for elem in dict:
            if elem['details'] > 6:
                if 'images' in elem:
                    current = {elem['title']: (elem['details'], elem['images'][0].get('uri')+'_8.jpg')}
                    resList.append(current)
    return resList

if __name__ == '__main__':
    main()


