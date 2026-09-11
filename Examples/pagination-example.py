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
signing_key = authenticationutils.load_signing_key('./certs/sandbox.p12', 'keystorepassword')
signer = MCSigner(CONSUMER_KEY, signing_key)

def fetch_data_from_api(base_url, initial_page=1, post_payload={}, signer=None, data=None):
    all_items = []
    current_page = initial_page
    total_items_downloaded = 0
    total_items = None

    while True:

        # Update the payload to include the current page number for pagination
        post_payload.update({"page": current_page, 'size': '10000'})

        # Perform a POST request to the API
        response = requests.post(base_url, params=post_payload, auth=signer, json=data)
        response_data = response.json()
        
        # Extract metadata
        current_page_number = response_data['currentPageNumber']
        total_pages = response_data['totalPages']
        total_items = response_data['totalItems']
        
        # Extract the actual items
        items = response_data.get('items', [])
        
        # Add the items from the current page to the master list
        all_items.extend(items)
        
        # Update the total number of items downloaded
        total_items_downloaded += len(items)
        
        # Print the current progress for reference
        print(f"Downloaded {len(items)} items from page {current_page_number}/{total_pages}.")
        
        # Check if we have reached the last page
        if current_page_number >= total_pages:
            break
        
        # Move to the next page
        current_page += 1

    # After the loop, verify that the number of downloaded items matches the totalItems value
    if total_items_downloaded == total_items:
        print(f"Successfully downloaded all {total_items_downloaded} items.")
    else:
        print(f"Warning: Downloaded {total_items_downloaded} items, but expected {total_items} items.")
    
    return all_items

all_records = fetch_data_from_api(base_url=f'{BASE_URL}/bin-ranges', initial_page=1, post_payload={}, signer=signer)

# Set up a file to store the results from the API
data_file = open('account_ranges.csv', 'w')
csv_writer = csv.writer(data_file)

# A for loop to go through the JSON objects and convert them into CSV rows
count = 0
for item in all_records:
    if count == 0:
        # Writing headers of CSV file
        header = item.keys()
        csv_writer.writerow(header)
        count += 1
    # Writing data of CSV file
    csv_writer.writerow(item.values())
 
data_file.close()
