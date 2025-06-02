from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Velora AI is running! <a href='/dashboard'>Go to Dashboard</a>"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/client/<phone_number>")
def client_page(phone_number):
    return render_template("client.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

