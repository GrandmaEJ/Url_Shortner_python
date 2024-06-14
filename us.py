from flask import request, jsonify, redirect
from utils import generate_short_id, log_missing_params, load_data, save_data, url_expired
import datetime
import random
import string

def init_routes(app):

    @app.route('/short', methods=['POST'])
    def create_short_url_post():
        data = request.json
        api_key = data.get('api')
        url = data.get('url')
        custom_id = data.get('Alice')

        if not api_key or not url:
            log_missing_params()
            return jsonify({"status": 505, "error": "Missing required parameters"}), 505

        data = load_data()

        if custom_id in [entry.get('Alice') for entry in data.values()]:
            return jsonify({"status": 505, "error": "Custom ID already exists. Please provide a different one."}), 505

        short_id = generate_short_id(url, custom_id)
        creation_time = datetime.datetime.now()
        expiry_time = creation_time + datetime.timedelta(days=30)

        data[short_id] = {
            "original_url": url,
            "creation_time": creation_time.isoformat(),
            "expiry_time": expiry_time.isoformat(),
            "Alice": custom_id
        }
        save_data(data)

        response = {
            "status": 200,
            "short_link": f"https://158.101.198.227:8398/{short_id}",
            "id": short_id,
            "redirect_link": url,
            "making_date_time": creation_time.strftime("%Y-%m-%d %H:%M:%S"),
            "expired_time": expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(response), 200

    @app.route('/short/api=<api_key>', methods=['GET'])
    def create_short_url_get(api_key):
        url = request.args.get('url')
        alice = request.args.get('Alice')

        if not api_key or not url:
            log_missing_params()
            return jsonify({"status": 505, "error": "Missing required parameters"}), 505

        data = load_data()

        if alice in [entry.get('Alice') for entry in data.values()]:
            return jsonify({"status": 505, "error": "Custom ID already exists. Please provide a different one."}), 505

        short_id = generate_short_id(url, alice)
        creation_time = datetime.datetime.now()
        expiry_time = creation_time + datetime.timedelta(days=30)

        data[short_id] = {
            "original_url": url,
            "creation_time": creation_time.isoformat(),
            "expiry_time": expiry_time.isoformat(),
            "Alice": alice
        }
        save_data(data)

        response = {
            "status": 200,
            "short_link": f"https://158.101.198.227:8398/{short_id}",
            "id": short_id,
            "redirect_link": url,
            "making_date_time": creation_time.strftime("%Y-%m-%d %H:%M:%S"),
            "expired_time": expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(response), 200

    @app.route('/<short_id>', methods=['GET'])
    def redirect_to_url(short_id):
        data = load_data()
        if short_id not in data or url_expired(data[short_id]["expiry_time"]):
            return jsonify({"status": 404, "error": "error occurrence"}), 404

        return redirect(data[short_id]["original_url"])

def generate_unique_custom_id(data):
    custom_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    while custom_id in data.values():
        custom_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return custom_id