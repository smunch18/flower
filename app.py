from flask import Flask, render_template, request
from openai import OpenAI 

app = Flask(__name__)

api_key = ''
with open("openai_key.txt","r") as w:
    api_key = w.readline()

# Set your OpenAI API key

client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)

"""@app.route('/', methods=['GET', 'POST'])

def capitalize_text():
    if request.method == 'POST':
        global user_input
        user_input = request.form['user_input']

        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "Extract the item the user is searching for and the users' location."},
                {"role": "user", "content": user_input}
            ],
            temperature= 0.2,
        )

        capitalized_text = completion.choices[0].message.content

        #capitalized_text = user_input.upper()
        return render_template('index2.html', capitalized_text=capitalized_text)
    return render_template('index2.html')



if __name__ == '__main__':
    app.run(debug=True)"""

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

    return chat_response

if __name__ == '__main__':
    app.run(debug=True)
