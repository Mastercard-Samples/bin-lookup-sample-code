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

# Params for loop
pageNum = 1
totalPages = 0
items = []

# Loop used to sequentially call the paginated API & build an array of account ranges
while pageNum != totalPages:
    params = {
    'page': pageNum,
    'size': 5000
    }

    resp = requests.post(
        f'{BASE_URL}/bin-ranges',
        auth=signer,
        params=params
    )
    pageNum = pageNum + 1
    totalPages = resp.json()['totalPages']
    items = items + resp.json()['items'] 

# Set up a file to store the results from the API
data_file = open('account_ranges.csv', 'w')
csv_writer = csv.writer(data_file)

# A for loop to go through the JSON objects and convert them into CSV rows
count = 0
for item in items:
    if count == 0:
        # Writing headers of CSV file
        header = item.keys()
        csv_writer.writerow(header)
        count += 1
    # Writing data of CSV file
    csv_writer.writerow(item.values())
 
data_file.close()