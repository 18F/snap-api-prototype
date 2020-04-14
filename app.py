import os
import json
from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from os import path

from snap_financial_factors.benefit_estimate import BenefitEstimate
from snap_financial_factors.input_data.parse_input_data import ParseInputData


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

        # Handle invalid input case; return error
        parsed_input_data = ParseInputData(raw_input_data).parse()
        if parsed_input_data.valid is False:
            return Response(
                response=json.dumps({
                    'errors': parsed_input_data.errors,
                    'status': 'ERROR',
                }),
                status=400,
                mimetype='application/json'
            )

        # Handle valid input case; return data
        input_data = parsed_input_data.result
        benefit_estimate = BenefitEstimate(input_data).calculate()

        use_pretty_print = raw_input_data.get('pretty_print', None)
        if use_pretty_print:
            pretty_print_kwargs = {'indent': 4}
        else:
            pretty_print_kwargs = {}

        return Response(
            response=json.dumps({
                **benefit_estimate,
                'status': 'OK',
            }, **pretty_print_kwargs),
            status=200,
            mimetype='application/json'
        )

    return app
