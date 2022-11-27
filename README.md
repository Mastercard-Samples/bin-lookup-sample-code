# BIN Lookup API - Code Examples

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Frameworks/Libraries](#frameworks)
- [How to Use](#instructions)
- [Support](#support)
- [License](#license)

## Overview  <a name="overview"></a>

This repo provides a set of examples in Python that demonstrate how to use the [BIN Lookup API](https://developer.mastercard.com/bin-table-resource/documentation/). There are 3 Python scripts that show you how to:

* Use the real-time single lookup endpoint
* Filter on the full data download endpoint
* Paginate through all data for a full download

## Requirements  <a name="requirements"></a>

- Python 3+

## Frameworks/Libraries <a name="frameworks"></a>
- [Requests](https://pypi.org/project/requests/)
- [Mastercard OAuth1 Signer](https://pypi.org/project/mastercard-oauth1-signer/)

## How to Use <a name="instructions"></a>

Once you have cloned this repo you can install the required dependencies with the following command:

```
pip install -r requirements.txt
```

Next, you will need to [create a Mastercard Developers project](https://developer.mastercard.com/platform/documentation/getting-started-with-mastercard-apis/quick-start-guide/#create) and adding the BIN Lookup API. This will give you a .p12 file, a consumer key, and key store credentials.

Add the .p12 file to the certs folder. Then, you can go to the Examples folder and select the script you want to use. Each script needs you to change the following:

* BASE_URL variable - this will be the Sandbox or Production URL for the API, which you can get from the docs on Mastercard Developers
* CONSUMER_KEY - this is the key that identifies you as a user, you can get it from your project on Mastercard Developers
* Keystore password - in the authenticationutils.load_signing_key method you need to pass this, it is a value shared with you privately when you are creating a project on Mastercard Developers 

Once you have the correct credentials you can run the script(s) usinng the following command:

```
python script_name.py
```

Each script will make a live call to the API using your credentials and demonstrate the response you get in each scenario.

## Support <a name="support"></a>
Please send an email to **apisupport@mastercard.com** with any questions or feedback you may have.

## License <a name="license"></a>
<p>Copyright 2022 Mastercard</p>
<p>Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at:</p>
<pre><code>   http://www.apache.org/licenses/LICENSE-2.0
</code></pre>
<p>Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.</p>