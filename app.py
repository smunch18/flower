from flask import Flask, render_template, request
from openai import OpenAI 
import googlemaps
import pandas as pd
import time

app = Flask(__name__)

api_key = ''
with open("openai_key.txt","r") as w:
    api_key = w.readline()

# Set your OpenAI API key

client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    response = respond(user_message)
    return response

def respond(user_message):
    """# Simple logic to generate response
    if "hi" in user_message.lower() or "hello" in user_message.lower() or "hey" in user_message.lower():
        return "Hi there!"
    elif "bye" in user_message.lower() or "goodbye" in user_message.lower():
        return "Goodbye!"
    else:
        return "I'm just a simple chatbot, I don't understand everything. Try saying hello or goodbye!"""
    
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "Extract the item the user is searching for and the users' location. Output format: item,location,'human message to user'. For example, vase,London,Oh! So you would like to find a vase in London? Here are some local places: (Do not always use this response, vary to sound more human.)"},
            {"role": "user", "content": user_message}
        ],
        temperature= 0.2,
    )

    response = completion.choices[0].message.content.split(',')

    # Extract search_item and user_location
    global search_item
    global user_location

    search_item = response[0].strip()
    user_location = response[1].strip()
    chat_response = response[2].strip()

    places = get_places(search_item, user_location)

    #somehow incorporate places into chat response output?

    return chat_response

def get_places(search_item, user_location):
    api_key = ''
    with open("googlemaps_key.txt","r") as w:
        api_key = w.readline()

    map_client = googlemaps.Client(api_key)

    #loc = tuple(input("Please write the latitude, longitude of where you're located: "))
    location = (44.23268671539581, -76.48910279456975) #random loc in kingston: 44.23268671539581, -76.48910279456975
    if " " in search_item:
        search_item = search_item.replace(" ", "")
    search_string = search_item  #str(input("What are you searching for? "))
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
    return df['names']

if __name__ == '__main__':
    app.run(debug=True)
