import os
from flask import Flask, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from os import path

from snap_financial_factors.benefit_estimate import BenefitEstimate
from snap_financial_factors.input_data.parse_input_data import ParseInputData


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/calculate": {"origins": "*"}})
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
        raw_input_data = request.get_json()

        # Handle invalid input case; return error
        parsed_input_data = ParseInputData(raw_input_data).parse()
        if parsed_input_data.valid is False:
            return jsonify({
                'status': 'ERROR',
                'errors': parsed_input_data.errors,
            }), 400

        # Handle valid input case; return data
        benefit_estimate = BenefitEstimate(parsed_input_data).calculate()
        return jsonify({
            **benefit_estimate,
            'status': 'OK',
        }), 200

    @app.route('/prescreener')
    @auth.login_required
    def prescreener():
        return render_template('prescreener.html')

    return app
