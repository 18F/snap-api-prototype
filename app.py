from flask import Flask, jsonify, request

from snap_financial_factors.benefit_estimate import BenefitEstimate

app = Flask(__name__)

@app.route('/')
def get_root():
    return jsonify(bbce_data), 300

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    input_data = request.get_json()
    benefit_estimate = BenefitEstimate(input_data)
    return jsonify(benefit_estimate.calculate()), 200