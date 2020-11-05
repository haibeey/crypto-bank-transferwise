import config, hmac, re,time,utils
from flask_restful import Resource, reqparse, request
from flask import current_app,jsonify
from flask_mail import Message
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import req


transfer_parser = reqparse.RequestParser()
transfer_parser.add_argument('account_number', required=True)
transfer_parser.add_argument('account_name', required=True)
transfer_parser.add_argument('amount', required=True)
transfer_parser.add_argument('bank_name', required=True)
transfer_parser.add_argument('source_currency')
transfer_parser.add_argument('target_currency')


class MakeTransfer(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        sign_data = request.headers.get("Sign Data")
        if not sign_data:
            return jsonify({"error":"No sign data passed in this request"}),400
        if not utils.verify(sign_data):
            return jsonify({"error":"Not authenticated"}),400
        data = transfer_parser.parse_args()
        acct_no = data.get('account_number')
        acct_name = data.get('account_name')
        amount = data.get('amount')
        bank_name = data.get('bank_name')
        sc = data.get('source_currency') or "GDP"
        tc = data.get('target_currency') or "NGN"

        return jsonify(req.transfer(acct_no,acct_name,amount,bank_name,source_currency=sc,target_currency=tc))

