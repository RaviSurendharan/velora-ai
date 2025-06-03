kimport json
import os
from datetime import datetime

# Simple file-based storage for MVP
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")

# Initialize files if they don’t exist
if not os.path.exists(CLIENTS_FILE):
    with open(CLIENTS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(CONVERSATIONS_FILE):
    with open(CONVERSATIONS_FILE, "w") as f:
        json.dump({}, f)

def get_clients():
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def get_client_by_phone(phone_number):
    clients = get_clients()
    return clients.get(phone_number)

def save_escort_profile(phone_number, name, style, bio, do_not_list, services):
    clients = get_clients()

    if phone_number not in clients:
        clients[phone_number] = {}

    clients[phone_number].update({
        "name": name,
        "style": style,
        "bio": bio,
        "do_not_list": do_not_list,
        "services": services,
        "updated_at": datetime.now().isoformat()
    })

    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f)

    return clients[phone_number]

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

def save_escort_profile(phone_number, name, style, bio, do_not_list, services):
    clients = get_clients()

    clients[phone_number] = {
        "name": name,
        "style": style,
        "bio": bio,
        "do_not_list": do_not_list,
        "services": services,
        "updated_at": datetime.now().isoformat()
    }

    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f)

    return clients[phone_number]

