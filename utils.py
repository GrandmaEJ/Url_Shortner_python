import hashlib
import json
import datetime



def generate_short_id(url, custom_id=None):
    if custom_id:
        return custom_id
    return hashlib.md5(url.encode()).hexdigest()[:6]

def log_missing_params():
    with open('log.txt', 'a') as log_file:
        log_file.write(f"Missing parameters: {datetime.datetime.now()}\n")


def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

def url_expired(expiry_time):
    return datetime.datetime.now() > datetime.datetime.fromisoformat(expiry_time)