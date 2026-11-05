"""
delta_example_helpers — reusable building blocks for the BinLookup delta tutorial.

auth    OAuth1 request signing (MCSigner, make_signer)
api     paginated, retrying HTTP calls (fetch_delta, download_snapshot_r)
delta   apply insert/update/delete operations to a snapshot (apply_delta)
fields  field-name matching and B'/R comparison (build_field_mapping, compare)
csv_io  CSV load/write (load_csv, write_csv_file)
config  JSON config loading/validation (load_config, get_signer_from_block)
"""
from .auth import MCSigner, make_signer
from .api import _get, _post, fetch_delta, download_snapshot_r
from .config import load_config, get_signer_from_block
from .csv_io import load_csv, write_csv_file
from .delta import NON_DATA, apply_delta, row_key
from .fields import build_field_mapping, compare, normalize_row

__all__ = [
    "MCSigner", "make_signer", "_get", "_post", "fetch_delta", "download_snapshot_r",
    "load_config", "get_signer_from_block", "load_csv", "write_csv_file", "NON_DATA",
    "apply_delta", "row_key", "build_field_mapping", "compare", "normalize_row",
]
