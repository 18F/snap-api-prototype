import os
import json
from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from os import path

from snap_financial_factors.benefit_estimate.snap_estimate_entrypoint import SnapEstimateEntrypoint


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/v0/calculate": {"origins": "*"}})
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
        return Response(
            response='welcome',
            status=300,
            mimetype='application/json'
        )

    @app.route('/v0/calculate', methods=['POST', 'GET'])
    @auth.login_required
    def calculate_from_json():
        json_data = request.get_json()
        args_data = request.args

        if json_data:
            raw_input_data = json_data
        elif args_data:
            raw_input_data = args_data.to_dict()
        else:
            raise ValueError('No input data received.')

        result = SnapEstimateEntrypoint(raw_input_data).calculate()

        if result['status'] == 'ERROR':
            return Response(
                response=json.dumps({
                    'errors': result['errors'],
                    'status': result['status'],
                }),
                status=400,
                mimetype='application/json'
            )

        use_pretty_print = raw_input_data.get('pretty_print', None)
        if use_pretty_print:
            pretty_print_kwargs = {'indent': 4}
        else:
            pretty_print_kwargs = {}

        return Response(
            response=json.dumps(result, **pretty_print_kwargs),
            status=200,
            mimetype='application/json'
        )

    return app
