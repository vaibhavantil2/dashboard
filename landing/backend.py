import urllib3
import simplejson as json
import http.client, urllib.request, urllib.parse, urllib.error, base64

reply_api_key = 'UMBs_SY2DqqnILtSQJv60g2'
reply_base_url = 'https://api.reply.io/v1/'

transit_api_key = '3833947c624b4eef9eccf542b4740213'
transit_base_url = 'api.wmata.com'

maxtrix_api_key = 'AIzaSyDjDg_7TM-NelBZsoKCfKz2xNFO0D1hsHY'
place_api_key = 'AIzaSyAKqU07QuZf1wezomzykkcSXiqeQNp-gyo'

api_key = '''put a reply.io api key in here'''
base_url = 'https://api.reply.io/v1/'


def get_campaigns():

    item = 'campaigns'

    url = '%s%s?apiKey=%s' % (reply_base_url, item, reply_api_key)

    http = urllib3.PoolManager()
    response = http.request('GET', url)

    json_items = json.loads(response.data)

    return json_items

#radius measured in meteres
def find_bus_stops(lat,lng,radius):

    headers = {
    'api_key': transit_api_key,
    }

    params = urllib.parse.urlencode({
        'Lat': lat,
        'Lon': lng,
        'Radius': radius,
    })

    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Bus.svc/json/jStops?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    json_items = json.loads(data)

    return json_items

def find_train_stations(lat,lng,radius):

    headers = {
        # Request headers
        'api_key': transit_api_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'Lat': lat,
        'Lon': lng,
        'Radius': radius,
    })

    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Rail.svc/json/jStationEntrances?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    json_items = json.loads(data)

    return json_items

def get_bus_predic(stop_id):

    headers = {
        'api_key': transit_api_key,
    }

    params = urllib.parse.urlencode({
        'StopID': stop_id,
    })

    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/NextBusService.svc/json/jPredictions?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    json_items = json.loads(data)

    return json_items

def get_train_predic(station_code):

    headers = {
        # Request headers
        'api_key': transit_api_key,
    }

    url = "/StationPrediction.svc/json/GetPrediction/%s?" % (station_code)

    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", url, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    json_items = json.loads(data)

    return json_items

def get_distance(start,dest):

     maxtrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'

     url = '%s&mode=walking&origins=%s&destinations=%s&key=%s' % (maxtrix_url, start, dest, maxtrix_api_key)

     http = urllib3.PoolManager()
     response = http.request('GET', url)

     json_items = json.loads(response.data)

     return(json_items)

def search_place(quer):

    place_base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='

    url = '%s%s&key=%s' % (place_base_url, quer, place_api_key)

    http = urllib3.PoolManager()
    response = http.request('GET', url)

    json_items = json.loads(response.data)

    lat = json_items['results'][0]['geometry']['location']['lat']
    lng = json_items['results'][0]['geometry']['location']['lng']

    return([lat,lng])
