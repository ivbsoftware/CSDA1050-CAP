import pandas as pd
import geopy as gp
import geocoder

#from geopy.geocoders import Nominatim, GeocodeFarm
#geolocator1 = Nominatim(user_agent="convert_geo.py")
#file2 = open('data_ready.csv', 'ab')
#geolocator = GeocodeFarm()
addresses = pd.read_csv("data_pre_ready.csv", sep=",", header=None, encoding='utf-8', engine='python')
#addresses = addresses.loc[0:1136]
addresses[15]="Null"

def returnxy(address):
    try:
        lat, lng = None, None
        #temp=address[0].to_string()
        if  not address[0] ==',':
            #location = geocoder.geolytica(address)
            location=geocoder.google(address,key='AIzaSyBzI1rP3XysBtUOhtrCvmyABe_CnX2pfL0')
            for feature in location.geojson['features']:
                lat=feature["properties"]["lat"]
                lng=feature["properties"]["lng"]
        else:
            exit()
    except:
        print("failed on address ",address)
        lat,lng = None,None
    return (lat,lng)

#print(addresses[13][i])
#test = geocoder.geolytica(addresses[13][1])
#for feature in test.geojson['features']:
    #print(feature["properties"]["lat"])
    #print(feature["properties"]["lng"])
for i in range(1,7380):
    test= returnxy(addresses[13][i])
    addresses[14][i] = test[0]
    addresses[15][i] = test[1]
    print(addresses[0][i])
    print(test[0])
    print(test[1])

addresses.to_csv('data_ready.csv',index=False)

#file2.close()
#addresses['long'] = addresses[13].apply(lambda x: x[1])
#addresses.to_csv('temp.csv')
