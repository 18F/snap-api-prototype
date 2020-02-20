from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from os import path

from snap_financial_factors.benefit_estimate import BenefitEstimate

if path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Auth not required locally, just in production.
    # Setting an AUTH_OFF flag to any value will turn off auth.
    auth_off = os.getenv('AUTH_OFF', False)

    if auth_off:
        return True

    # If auth is on, a username and password must be supplied
    # as environment variables.
    env_username = os.environ['USERNAME']
    env_password = os.environ['PASSWORD']

    if (username == env_username) and (password == env_password):
        return True

    return False

@app.route('/')
def get_root():
    return jsonify(bbce_data), 300

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    input_data = request.get_json()
    benefit_estimate = BenefitEstimate(input_data)
    return jsonify(benefit_estimate.calculate()), 200
