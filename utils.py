from flask import make_response, current_app,jsonify,request
import secrets, string, hmac, config,time,threading
from flask_jwt_extended import get_jwt_identity
import hashlib
from OpenSSL import crypto
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii


def nullOrZero(value):
    if value is None:
        return 0
    return value

def isFloat(value):
    try:
        float(value)
        return True
    except Exception:
        return False

def response(code, msg, data, token="", **kwargs):
    response = {"code": code, "message": msg, "data": data}
    if token:
        response["token"] = token
    for key in kwargs:
        response[key] = kwargs.get(key)
    return make_response(jsonify(response), code)

def catchExceptions(func):
    def catchAll(*args, **kwargs):
        current_app.logger.info("Announcing a request to the emperor (%s) ",request.headers)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            current_app.logger.info("Announcing a request error to the emperor. Details: %s",str(e))
            return response(400, "error while proccessing malformed data", [str(e)])

    return catchAll       

def signData(data):
    with open("private.pem") as f:
        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        return crypto.sign(priv_key, data.encode(), 'sha256')


def isByte(data):
    try:
        data.decode()
        return True
    except (UnicodeDecodeError, AttributeError):
        return False

def verify(signature):
    with open('authkeys.pem','r') as f:
        key = RSA.import_key(f.read())
        if not isByte(signature):
            signature = binascii.unhexlify(signature)
        hash = SHA256.new(b'cryptobankapi')
        verifier = PKCS115_SigScheme(key.publickey())
        try:
            verifier.verify(hash, signature)
            return True
        except:
            return False
