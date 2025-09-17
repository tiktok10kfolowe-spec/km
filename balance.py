import json
import os

BALANCE_FILE = "balances.json"

# Load balances or start empty
if os.path.exists(BALANCE_FILE):
    with open(BALANCE_FILE, "r") as f:
        try:
            balances = json.load(f)
        except:
            balances = {}
else:
    balances = {}

def save_balances():
    with open(BALANCE_FILE, "w") as f:
        json.dump(balances, f, indent=4)

def get_balance(user_id):
    user_id = str(user_id)
    if user_id not in balances:
        balances[user_id] = 0.0  # new users start with $0
        save_balances()
    return float(balances[user_id])

def update_balance(user_id, amount):
    user_id = str(user_id)
    balances[user_id] = get_balance(user_id) + float(amount)
    save_balances()
    return float(balances[user_id])

def set_balance(user_id, amount):
    user_id = str(user_id)
    balances[user_id] = float(amount)
    save_balances()
    return float(balances[user_id])