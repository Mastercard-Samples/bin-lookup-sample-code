"""Loading and validation for the tutorial's JSON config file."""
import json


def load_config(path):
    """Load the JSON config file and validate the flat credential layout."""
    with open(path, encoding="utf-8") as config_file:
        config = json.load(config_file)
    if "host" not in config:
        raise ValueError("Config missing 'host'.")
    for field in ("consumerKey", "keystoreP12Path", "keystorePassword"):
        if field not in config:
            raise ValueError(f"Config missing '{field}'.")
    return config


def get_signer_from_block(credentials_block, block_name="customer"):
    """Validate a credentials block and return (consumerKey, p12Path, password)."""
    for field in ("consumerKey", "keystoreP12Path", "keystorePassword"):
        if field not in credentials_block:
            raise ValueError(f"Config '{block_name}' block missing: '{field}'")
    return credentials_block["consumerKey"], credentials_block["keystoreP12Path"], credentials_block["keystorePassword"]
