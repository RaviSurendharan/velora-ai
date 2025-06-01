from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Velora AI is running!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
