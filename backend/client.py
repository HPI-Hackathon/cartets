# Client thread started for each player
import urllib2
import json

def main(ll):
    response = urllib2.urlopen('http://m.mobile.de/svc/s/?ll=' + ll)
    data = json.load(response)['items']
    gameCars = validation(data)
    print gameCars

def validation(dict):
    resList = []
    while len(resList) <= 20:
        for elem in dict:
            if elem['details'] > 6:
                resList.append(elem['details'])
    return resList

if __name__ == '__main__':
    main()


