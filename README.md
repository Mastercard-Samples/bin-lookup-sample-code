# BIN Lookup API - Code Examples

## Overview

This repository contains Python examples for the [BIN Lookup API](https://developer.mastercard.com/bin-table-resource/documentation/). The sample scripts demonstrate three common use cases:

- single real-time BIN lookup
- filtered data retrieval from the full download endpoint
- paginated download of all BIN range records

## Requirements

- Python 3.x
- Access to a Mastercard Developer project with the BIN Lookup API enabled
- A valid `.p12` certificate file and consumer key from Mastercard Developers

## Dependencies

This project uses the following Python packages:

- [Requests](https://pypi.org/project/requests/)
- [Mastercard OAuth1 Signer](https://pypi.org/project/mastercard-oauth1-signer/)

Install them with:

```bash
pip install -r requirements.txt
```

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── certs/
│   └── your.p12
├── Examples/
│   ├── single-lookup-example.py
│   ├── filtering-example.py
│   └── pagination-example.py
```

## Setup

1. Clone the repository.
2. Create a Mastercard Developers project and add the BIN Lookup API.
3. Download the project credentials, including:
   - the `.p12` certificate file
   - the consumer key
   - the keystore password
4. Place the `.p12` file in the `certs` folder.
5. Update the following values in the script you want to run:
   - `BASE_URL` - Sandbox or production API base URL
   - `CONSUMER_KEY` - your Mastercard project consumer key
   - keystore password in `authenticationutils.load_signing_key(...)`

Each script contains placeholder values that you must replace before running it.

## Examples

### 1. Single Lookup

File: `Examples/single-lookup-example.py`

This example prompts for an 8-digit BIN and submits a POST request to the account search endpoint.

Run it with:

```bash
python Examples/single-lookup-example.py
```

### 2. Filtering

File: `Examples/filtering-example.py`

This example posts filter criteria to the BIN range endpoint and returns the total number of matching items.

Run it with:

```bash
python Examples/filtering-example.py
```

### 3. Pagination

File: `Examples/pagination-example.py`

This example downloads all BIN range records across pages and writes the results to a CSV file named `account_ranges.csv` in the project directory.

Run it with:

```bash
python Examples/pagination-example.py
```

## Notes

- The sample scripts make live API calls using your credentials.
- The `BASE_URL` value must match the environment you are targeting, such as Sandbox or Production.
- The keystore password is sensitive and should be kept private.

## Support

Please email **apisupport@mastercard.com** with any questions or feedback.

## License

Copyright 2022 Mastercard

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
