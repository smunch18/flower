import googlemaps
import pandas as pd
import time
    
api_key = ''
with open("googlemaps_key.txt","r") as w:
    api_key = w.readline()
map_client = googlemaps.Client(api_key)

#loc = tuple(input("Please write the latitude, longitude of where you're located: "))
location = (44.23268671539581, -76.48910279456975) #random loc in kingston: 44.23268671539581, -76.48910279456975
search_string = "flowerpot" #str(input("What are you searching for? "))
distance = 1500 #15km

business_list = []

response = map_client.places_nearby(location=location, keyword=search_string, radius=distance)

#print(response.get('results'))

business_list.extend(response.get('results'))
next_page_token = response.get('next_page_token')

while next_page_token:
    time.sleep(2)
    response = map_client.places_nearby(location=location, keyword=search_string, radius=distance, page_token=next_page_token)
    business_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

df = pd.DataFrame(business_list)
#print(df['place_id'])
#print(df.columns)
place_id = df['place_id']
df['url'] = 'www.google.com/maps/place/?q=place_id:' + place_id
#df.to_excel('item shop list.xlsx', index=False)
#df.sort_values("")

print(df['name'].head(10))
#print(df['url'].head(5))
#df['geometry']

#FURTHER STUFF
"""could use googlemaps distance matrix api to figure out distance of places from user's location, then sort entries based on that column"""