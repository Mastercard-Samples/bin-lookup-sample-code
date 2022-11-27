import requests
from requests.auth import AuthBase
import oauth1.authenticationutils as authenticationutils
from oauth1.signer import OAuthSigner
import csv

BASE_URL = 'Add Sandbox or Production BASE URL here'
CONSUMER_KEY = 'Add you project consumer key here' 

# MCSigner
# Helper class for signing request objects
class MCSigner(AuthBase):
    def __init__(self, consumer_key, signing_key):
        self.signer = OAuthSigner(consumer_key, signing_key)

    def __call__(self, request):
        self.signer.sign_request(request.url, request)
        return request

# Generate a signing key and use it, and consumer key, with the signer class
signing_key = authenticationutils.load_signing_key('./certs/your.p12', 'keystorepassword')
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

print (f"There are {resp.json()['totalItems']} items that match")