import unittest
import json
import os,io
from time import sleep
from datetime import datetime
import config,utils
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
from run import  *


app_client=create_app("config").test_client()

class AppTests(unittest.TestCase):
    def test_make_transfer(self):
        with open('authkeys.pem','r') as f:
            key = RSA.import_key(f.read())
        hash = SHA256.new(b'cryptobankapi')
        signer = PKCS115_SigScheme(key)
        signature = signer.sign(hash)

        resp=app_client.post("/make/transfer/", data=dict(
            account_number="12345678",
            account_name="Abjoe Abraham",
            amount=10000,
            bank_name="Hsbc Bank Plc",
            source_currency="GBP",
            target_currency="GBP"
        ),headers={"Sign Data": binascii.hexlify(signature)}) 
        
        res = json.loads(resp.data.decode())
        self.assertTrue(json.loads(res.get("response")).get("status")=="COMPLETED")
    def test_signing(self):
        print(utils.signData("abraham"))
    
        