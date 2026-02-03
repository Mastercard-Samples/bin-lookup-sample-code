import requests
from requests.auth import AuthBase
import oauth1.authenticationutils as authenticationutils
from oauth1.signer import OAuthSigner
import csv

BASE_URL = 'https://sandbox.api.mastercard.com/binlookup/v2'
CONSUMER_KEY = 'dq1RlXUmeqfHOXz3iCs_JM4cYXRpJVgvp_wzcw9Qb3a3c479!af2d2e8007f9409586e006241d1928960000000000000000' 

# MCSigner
# Helper class for signing request objects
class MCSigner(AuthBase):
    def __init__(self, consumer_key, signing_key):
        self.signer = OAuthSigner(consumer_key, signing_key)

    def __call__(self, request):
        self.signer.sign_request(request.url, request)
        return request

# Generate a signing key and use it, and consumer key, with the signer class
# signing_key = authenticationutils.load_signing_key('./certs/your.p12', 'keystorepassword') ## Comentado por mi
signing_key = authenticationutils.load_signing_key(
    r"C:\Users\Usuario\OneDrive\Desktop\Mastercard\Mastercard key\p12\matias-cert.p12",
    "020122.C@ssi"
)


signer = MCSigner(CONSUMER_KEY, signing_key)

print("Enter a 8 digit BIN:")
bin = input()

lookup_bin = {
  "accountRange": bin
}

resp = requests.post(
        f'{BASE_URL}/bin-ranges/account-searches',
        auth=signer,
        json = lookup_bin
    )

print (resp.json())