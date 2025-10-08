from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS (Cross-Origin Resource Sharing) to allow your front-end (index.html)
# to communicate with this backend, even if they are run from different places.
CORS(app)

@app.route('/')
def home():
    """
    A simple route to easily check if the server is up and running.
    You can visit this in your browser.
    """
    return "<h1>Nyay Sahayak Backend is running!</h1>"

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    This is the main API endpoint that your front-end will interact with.
    It receives a message from the user and will eventually send back the AI's response.
    """
    # Get the JSON data sent from the front-end
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    # Extract the user's message from the JSON payload
    user_message = data.get('message')

    # --- PHASE 3: AI and Database logic will go here ---
    # For now, we'll just create a simple, hardcoded response
    # to confirm that the connection is working.
    print(f"Received message: {user_message}") # Log to terminal for debugging
    bot_response = f"The backend has successfully received your message: '{user_message}'"

    # Send the response back to the front-end in JSON format
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    # This makes the server run.
    # debug=True allows the server to auto-reload when you save changes.
    # port=5000 specifies the port to run on.
    # You will access your server at http://127.0.0.1:5000
    app.run(debug=True, port=5000)
