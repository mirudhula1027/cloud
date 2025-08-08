from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def hello():
    """Return a friendly greeting."""
    return "Welcome to my Flask app!"

@app.route("/goodbye")
def goodbye():
    """Return a goodbye message."""
    return "Goodbye! See you next time."

@app.route("/ask", methods=["POST"])
def ask():
    """Receive a prompt via JSON, return OpenAI's response."""
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in JSON body"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 8080))
    app.run(host=host, port=port, debug=True)
