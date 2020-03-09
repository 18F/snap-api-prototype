import os
from flask import Flask, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth
from os import path

from snap_financial_factors.benefit_estimate import BenefitEstimate


def create_app():
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    if path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()

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
    @auth.login_required
    def get_root():
        return jsonify('welcome'), 300

    @app.route('/calculate', methods=['POST', 'GET'])
    @auth.login_required
    def calculate_from_json():
        input_data = request.get_json()
        benefit_estimate = BenefitEstimate(input_data)
        return jsonify(benefit_estimate.calculate()), 200

    @app.route('/prescreener')
    @auth.login_required
    def prescreener():
        return render_template('prescreener.html')

    return app
