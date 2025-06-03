from flask import Flask, request, jsonify, render_template
import os
from ai.chat import process_message
from messaging.sms import send_sms
from twilio.twiml.messaging_response import MessagingResponse
import database.models as db
from auth import auth_bp


app = Flask(__name__)
app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return "Velora AI is running! <a href='/dashboard'>Go to Dashboard</a>"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/client/<phone_number>")
def client_page(phone_number):
    return render_template("client.html")

@app.route("/test-ai", methods=["GET"])
def test_ai():
    # Simple endpoint to test the AI
    test_message = request.args.get("message", "Hello")
    response = process_message(test_message)
    return jsonify({"message": test_message, "response": response})

@app.route("/sms", methods=["POST"])
def sms_webhook():
    """Handle incoming SMS messages"""
    from_number = request.values.get("From", "")
    body = request.values.get("Body", "")
    
    print(f"Received message from {from_number}: {body}")
    
    # Check if the client exists
    client = db.get_client_by_phone(from_number)
    
    # If new, create default profile
    if not client:
        client = db.save_client(
            phone_number=from_number,
            name="New Client",
            style="friendly"
        )
    
    # Save client's message
    db.save_message(from_number, body, is_client=True)
    
    # Get conversation history
    conversation = db.get_conversation(from_number)

    # 💡 Use selected personality style
    ai_response = process_message(body, conversation, client)
    
    # Save AI's reply
    db.save_message(from_number, ai_response, is_client=False)

    # Send back response via Twilio
    resp = MessagingResponse()
    resp.message(ai_response)
    
    return str(resp)

@app.route("/clients", methods=["GET"])
def list_clients():
    """List all clients"""
    clients = db.get_clients()
    return jsonify(clients)

@app.route("/clients/<phone_number>", methods=["GET"])
def get_client(phone_number):
    """Get client details"""
    client = db.get_client_by_phone(phone_number)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    # Get conversation history
    conversation = db.get_conversation(phone_number)
    
    return jsonify({
        "client": client,
        "conversation": conversation
    })

@app.route("/clients/<phone_number>", methods=["POST"])
def add_client(phone_number):
    """Add or update a client"""
    data = request.json
    
    client = db.save_client(
        phone_number=phone_number,
        name=data.get("name", "New Client"),
        style=data.get("style", "friendly"),
        do_not_list=data.get("do_not_list", []),
        services=data.get("services", [])
    )
    
    return jsonify(client)

@app.route("/send-message/<phone_number>", methods=["POST"])
def send_message_to_client(phone_number):
    """Send a message to a client"""
    data = request.json
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    # Get client
    client = db.get_client_by_phone(phone_number)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    # Send SMS
    result = send_sms(phone_number, message)
    
    if result.get("success", False):
        # Save message to conversation history
        db.save_message(phone_number, message, is_client=False)
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to send message", "details": result.get("error")}), 500

@app.route("/test-sms", methods=["GET"])
def test_sms():
    """Test endpoint to send an SMS"""
    to_number = request.args.get("to", "")
    message = request.args.get("message", "Hello from Velora AI!")
    
    if not to_number:
        return jsonify({"error": "Missing 'to' parameter"}), 400
    
    result = send_sms(to_number, message)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

