import json
import os

import requests
from requests.auth import AuthBase
import oauth1.authenticationutils as authenticationutils
from oauth1.signer import OAuthSigner

EXAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(EXAMPLES_DIR, "config.json")

with open(CONFIG_PATH, encoding="utf-8") as config_file:
    config = json.load(config_file)

BASE_URL = config["host"]
CONSUMER_KEY = config["consumerKey"]
KEYSTORE_PATH = config["keystoreP12Path"]
KEYSTORE_PASSWORD = config["keystorePassword"]

# MCSigner
# Helper class for signing request objects
class MCSigner(AuthBase):
    def __init__(self, consumer_key, signing_key):
        self.signer = OAuthSigner(consumer_key, signing_key)

    def __call__(self, request):
        self.signer.sign_request(request.url, request)
        return request

# Generate a signing key and use it, and consumer key, with the signer class
signing_key = authenticationutils.load_signing_key(KEYSTORE_PATH, KEYSTORE_PASSWORD)
signer = MCSigner(CONSUMER_KEY, signing_key)

filters = [
    {
        "key": "customerName",
        "value": "CITIBANK N.A."
    },
    {
        "key": "productCode",
        "value": "MCO"
    }
]

resp = requests.post(
        f'{BASE_URL}/bin-ranges',
        auth=signer,
        json = filters
    )

print(f"There are {resp.json()['totalItems']} items that match")