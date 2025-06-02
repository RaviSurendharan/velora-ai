from flask import Flask, request, jsonify, render_template
import os
from ai.chat import process_message

app = Flask(__name__)

@app.route("/")
def home():
    return "Velora AI is running!"

@app.route("/test-ai", methods=["GET"])
def test_ai():
    test_message = request.args.get("message", "Hello")
    response = process_message(test_message)
    return jsonify({"message": test_message, "response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
