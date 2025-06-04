import json
import os
from datetime import datetime

# Setup data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")
ESCORTS_FILE = os.path.join(DATA_DIR, "escorts.json")

# Initialize files if not exist
for file_path in [CLIENTS_FILE, CONVERSATIONS_FILE, ESCORTS_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)

# --- Clients ---
def get_clients():
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def get_client_by_phone(phone_number):
    clients = get_clients()
    return clients.get(phone_number)

def save_client(phone_number, name="New Client", style="friendly", do_not_list=None, services=None):
    clients = get_clients()
    clients[phone_number] = {
        "name": name,
        "style": style,
        "do_not_list": do_not_list or [],
        "services": services or [],
        "updated_at": datetime.now().isoformat()
    }
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f)
    return clients[phone_number]

# --- Conversations ---
def get_conversations():
    with open(CONVERSATIONS_FILE, "r") as f:
        return json.load(f)

def get_conversation(phone_number):
    conversations = get_conversations()
    return conversations.get(phone_number, [])

def save_message(phone_number, content, is_client=True):
    conversations = get_conversations()
    if phone_number not in conversations:
        conversations[phone_number] = []
    conversations[phone_number].append({
        "content": content,
        "is_client": is_client,
        "timestamp": datetime.now().isoformat()
    })
    with open(CONVERSATIONS_FILE, "w") as f:
        json.dump(conversations, f)
    return conversations[phone_number]

# --- Escorts ---
def get_escorts():
    with open(ESCORTS_FILE, "r") as f:
        return json.load(f)

def get_escort(phone_number):
    escorts = get_escorts()
    return escorts.get(phone_number)

def save_escort(phone_number, name, password, style="", bio="", do_not_list=None, services=None):
    escorts = get_escorts()
    escorts[phone_number] = {
        "name": name,
        "password": password,
        "style": style,
        "bio": bio,
        "do_not_list": do_not_list or [],
        "services": services or [],
        "updated_at": datetime.now().isoformat()
    }
    with open(ESCORTS_FILE, "w") as f:
        json.dump(escorts, f)
    return escorts[phone_number]
