import requests
import argparse

key = 'd4a3de1c8ee312e598ff9bbb1da20388'
parser = argparse.ArgumentParser(description='Choose city.')
parser.add_argument('-i', dest='id', help='City id')
parser.add_argument('-l', dest='loc', help='City location')
args = parser.parse_args()

if args.id:
    myResponse = requests.get('http://api.openweathermap.org/data/2.5/weather?id={0}&APPID={1}'.format(args.id, key))
elif args.loc:
    myResponse = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}'.format(args.loc, key))
myResponse = myResponse.json()
try:
    print('Current temp in {1}: {0}° C'.format(myResponse['main']['temp'] - 273.15, myResponse['name']))
except:
    pass
