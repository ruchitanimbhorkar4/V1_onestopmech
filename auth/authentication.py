import json
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def load_data(filename):
    filepath = os.path.join(DATA_PATH, filename)
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_data(filename, data):
    filepath = os.path.join(DATA_PATH, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def email_exists(email, filename):
    users = load_data(filename)
    for user_data in users.values():
        if user_data.get('email') == email:
            return True
    return False

def username_exists(username, filename):
    users = load_data(filename)
    return username in users

def save_user_with_username(username, email, hashed_password, contact, role, filename):
    try:
        users = load_data(filename)
        users[username] = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "contact": contact,
            "role": role
        }
        save_data(filename, users)
        return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False

def authenticate_user_by_username_or_email(identifier, password, filename):
    users = load_data(filename)
    
    # Try to find user by username first
    if identifier in users:
        user = users[identifier]
        if verify_password(password, user['password']):
            return True, user, identifier
    
    # If not found by username, try by email
    for username, user_data in users.items():
        if user_data.get('email') == identifier:
            if verify_password(password, user_data['password']):
                return True, user_data, username
    
    return False, {}, ""

def authenticate_user(email, password, filename):
    return authenticate_user_by_username_or_email(email, password, filename)

def save_user(email, hashed_password, contact, role, filename):
    return save_user_with_username(email, email, hashed_password, contact, role, filename)
