from flask import Flask, request, jsonify
import os
from ai.chat import process_message
from messaging.sms import send_sms
from twilio.twiml.messaging_response import MessagingResponse
import database.models as db

app = Flask(__name__)

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

    client = db.get_client_by_phone(from_number)

    if not client:
        client = db.save_client(
            phone_number=from_number,
            name="New Client",
            style="friendly"
        )

    db.save_message(from_number, body, is_client=True)
    conversation = db.get_conversation(from_number)

    ai_response = process_message(body, conversation, client)

    db.save_message(from_number, ai_response, is_client=False)

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

@app.route("/clients", methods=["GET"])
def list_clients():
    clients = db.get_clients()
    return jsonify(clients)

@app.route("/clients/<phone_number>", methods=["GET"])
def get_client(phone_number):
    client = db.get_client_by_phone(phone_number)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    conversation = db.get_conversation(phone_number)

    return jsonify({
        "client": client,
        "conversation": conversation
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
