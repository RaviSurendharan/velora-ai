from flask import Flask, request, jsonify, render_template
import os
from ai.chat import process_message
from messaging.sms import send_sms
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Simple in-memory storage for conversation history
conversations = {}

@app.route("/")
def home():
    return "Velora AI is running!"

@app.route("/test-ai", methods=["GET"])
def test_ai():
    test_message = request.args.get("message", "Hello")
    response = process_message(test_message)
    return jsonify({"message": test_message, "response": response})

@app.route("/sms", methods=["POST"])
def sms_webhook():
    from_number = request.values.get("From", "")
    body = request.values.get("Body", "")

    print(f"Received message from {from_number}: {body}")

    if from_number not in conversations:
        conversations[from_number] = []

    conversations[from_number].append({
        "is_client": True,
        "content": body
    })

    client_profile = {"name": "Your Name", "style": "friendly"}
    ai_response = process_message(body, conversations[from_number], client_profile)

    conversations[from_number].append({
        "is_client": False,
        "content": ai_response
    })

    resp = MessagingResponse()
    resp.message(ai_response)

    return str(resp)

@app.route("/test-sms", methods=["GET"])
def test_sms():
    to_number = request.args.get("to", "")
    message = request.args.get("message", "Hello from Velora AI!")

    if not to_number:
        return jsonify({"error": "Missing 'to' parameter"}), 400

    result = send_sms(to_number, message)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
