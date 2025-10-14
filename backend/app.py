import os
import openai  # Import the OpenAI library
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for cross-origin requests
CORS(app)

# --- Configure the OpenAI API ---
# Set your OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the key exists and configure the client
if not OPENAI_API_KEY:
    raise ValueError("No OPENAI_API_KEY found in environment variables. Please set it in your .env file.")
openai.api_key = OPENAI_API_KEY

# Initialize the OpenAI client (using the modern openai library >v1.0)
client = openai.OpenAI()


# --- System Prompt for the AI ---
# This remains the same as it defines the chatbot's behavior.
SYSTEM_PROMPT = """
You are 'Nyay Sahayak', a friendly, empathetic, and knowledgeable legal assistant chatbot for the Indian context. 
Your primary goal is to simplify complex legal information and guide users.
You MUST communicate in simple, clear language, avoiding technical jargon.
Your personality is helpful, reassuring, and professional.

Based on the user's message, you must first understand their 'intent'. The possible intents are:
1.  'fir_writer': User wants help writing an FIR.
2.  'law_finder': User is describing a problem and wants to know the relevant laws.
3.  'rights_guide': User is asking about their legal rights.
4.  'doc_demystifier': User wants an explanation of a legal document.
5.  'greeting_or_smalltalk': The user is just saying hi or making small talk.

After identifying the intent, provide a direct, helpful response. 
- If the intent is 'fir_writer', respond with: "I can definitely help you draft a First Information Report (FIR). To get started, please tell me in your own words what happened."
- If the intent is 'law_finder', 'rights_guide', or 'doc_demystifier', provide a concise, simplified explanation based on their query.
- If it's small talk, respond with a friendly, appropriate message.

Your response should be just the text you want to show the user. Do not mention the intent analysis in your final response.
"""


@app.route('/')
def home():
    """ A simple route to check if the server is running. """
    return "<h1>Nyay Sahayak AI Backend (powered by OpenAI) is running!</h1>"


@app.route('/api/chat', methods=['POST'])
def chat():
    """ Main API endpoint for chat, now powered by OpenAI. """
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data.get('message')
    print(f"Received message: {user_message}")

    try:
        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # A powerful and cost-effective model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract the response text
        bot_response = response.choices[0].message.content.strip()
        print(f"AI Response: {bot_response}")

        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = "Sorry, I'm having trouble connecting to my brain right now. Please check your OpenAI API key and server configuration."
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

