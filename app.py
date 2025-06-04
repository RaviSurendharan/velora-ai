from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import database.models as db

from ai.chat import process_message
from messaging.sms import send_sms
from twilio.twiml.messaging_response import MessagingResponse
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "velora-secret-key"  # Secure key for session

app.register_blueprint(auth_bp)

# 🏠 Landing Page
@app.route("/")
def home():
    return render_template("home.html")

# 📲 Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 📱 Client Page
@app.route("/client/<phone_number>")
def client_page(phone_number):
    return render_template("client.html")

# 🤖 AI Test Route
@app.route("/test-ai", methods=["GET"])
def test_ai():
    test_message = request.args.get("message", "Hello")
    response = process_message(test_message)
    return jsonify({"message": test_message, "response": response})

# 📩 SMS Webhook
@app.route("/sms", methods=["POST"])
def sms_webhook():
    from_number = request.values.get("From", "")
    body = request.values.get("Body", "")

    client = db.get_client_by_phone(from_number)
    if not client:
        client = db.save_client(phone_number=from_number, name="New Client", style="friendly")

    escort = db.get_escort(from_number)
    db.save_message(from_number, body, is_client=True)

    conversation = db.get_conversation(from_number)
    ai_response = process_message(body, conversation, client, escort)
    db.save_message(from_number, ai_response, is_client=False)

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

# 📋 Clients API
@app.route("/clients", methods=["GET"])
def list_clients():
    return jsonify(db.get_clients())

@app.route("/clients/<phone_number>", methods=["GET"])
def get_client(phone_number):
    client = db.get_client_by_phone(phone_number)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    conversation = db.get_conversation(phone_number)
    return jsonify({"client": client, "conversation": conversation})

@app.route("/clients/<phone_number>", methods=["POST"])
def add_client(phone_number):
    data = request.json
    client = db.save_client(
        phone_number=phone_number,
        name=data.get("name", "New Client"),
        style=data.get("style", "friendly"),
        do_not_list=data.get("do_not_list", []),
        services=data.get("services", [])
    )
    return jsonify(client)

# 📤 Manual SMS Send
@app.route("/send-message/<phone_number>", methods=["POST"])
def send_message_to_client(phone_number):
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message is required"}), 400

    client = db.get_client_by_phone(phone_number)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    result = send_sms(phone_number, message)
    if result.get("success", False):
        db.save_message(phone_number, message, is_client=False)
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to send message", "details": result.get("error")}), 500

@app.route("/test-sms", methods=["GET"])
def test_sms():
    to_number = request.args.get("to", "")
    message = request.args.get("message", "Hello from Velora AI!")
    if not to_number:
        return jsonify({"error": "Missing 'to' parameter"}), 400
    return jsonify(send_sms(to_number, message))

# 👩 Escort Profile
@app.route("/escort-profile", methods=["GET", "POST"])
def escort_profile():
    phone_number = session.get("escort_phone")
    if not phone_number:
        return redirect(url_for("escort_login"))

    escort = db.get_escort(phone_number)
    if not escort:
        return redirect(url_for("escort_login"))

    if request.method == "POST":
        escort["name"] = request.form.get("name")
        escort["style"] = request.form.get("style")
        escort["bio"] = request.form.get("bio")
        escort["services"] = [s.strip() for s in request.form.get("services", "").split(",")]
        escort["do_not_list"] = [d.strip() for d in request.form.get("do_not_list", "").split(",")]

        db.save_escort(
            phone_number,
            escort["name"],
            escort.get("password", ""),
            escort["style"],
            escort["bio"],
            escort["do_not_list"],
            escort["services"]
        )

    return render_template("escort_profile.html", escort=escort)

# 📝 Signup
@app.route("/escort-signup", methods=["GET", "POST"])
def escort_signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        password = request.form.get("password")

        escorts = db.get_escorts()
        if
