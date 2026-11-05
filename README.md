# BIN Lookup API - Code Examples

## Overview

This repository contains Python examples for the [BIN Lookup API](https://developer.mastercard.com/bin-table-resource/documentation/). The sample scripts demonstrate four common use cases:

- single real-time BIN lookup
- filtered data retrieval from the full download endpoint
- paginated download of all BIN range records
- delta validation against the live BIN ranges

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
│   ├── config.json
│   ├── single-lookup-example.py
│   ├── filtering-example.py
│   ├── pagination-example.py
│   ├── delta-example.py
│   └── delta-example-helpers/
```

## Setup

1. Clone the repository.
2. Create a Mastercard Developers project and add the BIN Lookup API.
3. Download the project credentials, including:
   - the `.p12` certificate file
   - the consumer key
   - the keystore password
4. Place the `.p12` file in the `certs` folder.
5. Update the shared credentials in [Examples/config.json](Examples/config.json) with your project values:
   - `consumerKey` - your Mastercard project consumer key
   - `keystoreP12Path` - full path to your `.p12` certificate
   - `keystorePassword` - your keystore password

The scripts all read from this shared config file.

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

This example posts filter criteria to the BIN range endpoint and returns the total number of matching items. You can edit the filter list in the script before running it:

```python
filters = [
    {"key": "customerName", "value": "Crown Credit Bank 4"},
    {"key": "productCode", "value": "MUS"}
]
```

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

### 4. Delta Validation

File: `Examples/delta-example.py`

This example validates a local base snapshot by applying a delta and comparing the resulting data to the live BIN range results. It uses the local snapshot `Examples/snapshot_3355.csv`.

Run it with:

```bash
python Examples/delta-example.py --config Examples/config.json --input-snapshot-base Examples/snapshot_3355.csv --save-csv
```

The helper package used by this example lives in `Examples/delta-example-helpers` and is installed automatically when you install the repository requirements.

## Notes

- The sample scripts make live API calls using your credentials.
- The `BASE_URL` value must match the environment you are targeting, such as Sandbox or Production.
- The keystore password is sensitive and should be kept private.

## Support

Email DBN.BinTableResource.Support@mastercard.com with any questions or feedback.

## License

Copyright 2026 Mastercard

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
