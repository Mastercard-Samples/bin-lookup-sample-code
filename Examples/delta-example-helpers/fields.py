"""Field name normalization and B'/R comparison helpers."""
import ast
import json
import re
from .delta import row_key

# The public /bin-ranges endpoint omits these fields from its JSON response
# entirely when they hold their type's default (falsy) value — booleans
# omitted when false, binLength omitted when 0 — serializing them as blank.
# Other sources (e.g. the admin snapshot export) write the default out
# explicitly. Map each such field to the canonical string its blank form
# represents, so blank and explicit-default compare equal.
FIELD_DEFAULTS_WHEN_BLANK = {
    "smartDataEnabled": "false",
    "localUse": "false",
    "authorizationOnly": "false",
    "governmentRange": "false",
    "nonReloadableIndicator": "false",
    "gamblingBlockEnabled": "false",
    "binLength": "0",
}

# Fields holding a nested structure (e.g. "country") that different sources
# stringify differently — valid JSON (double-quoted) vs. Python dict-repr
# (single-quoted) — even though the underlying data is identical.
STRUCTURED_FIELDS = {"country"}


def _canonical_structured_value(text):
    """Parse a stringified structure (JSON or Python repr) into comparable data."""
    for parser in (json.loads, ast.literal_eval):
        try:
            return parser(text)
        except (ValueError, SyntaxError):
            continue
    return text


def _canonical_value(field, value):
    """
    Canonicalize a field value for equality comparison.

    Normalizes boolean casing (True/true, False/false), treats a blank value
    as equal to the field's known default when the public API omits default
    values from its response (see FIELD_DEFAULTS_WHEN_BLANK), and parses
    structured fields (see STRUCTURED_FIELDS) so differing stringification
    styles (JSON vs. Python repr) of the same data compare equal.
    """
    text = str(value).strip() if value is not None else ""
    if field in STRUCTURED_FIELDS and text:
        return _canonical_structured_value(text)
    lowered = text.lower()
    if lowered in ("true", "false"):
        return lowered
    if text == "" and field in FIELD_DEFAULTS_WHEN_BLANK:
        return FIELD_DEFAULTS_WHEN_BLANK[field]
    return text


def _norm(name):
    """Lowercase and strip non-alphanumeric characters, for fuzzy field-name matching."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def build_field_mapping(b_fields, r_fields):
    """Map each B field name to its equivalent R field name, matched by normalized name."""
    r_by_normalized_name = {_norm(field): field for field in r_fields}
    return {
        field: r_by_normalized_name[_norm(field)]
        for field in b_fields
        if _norm(field) in r_by_normalized_name
    }


def normalize_row(row, field_mapping):
    """Re-key a row from B's field names to R's field names."""
    return {r_name: str(row.get(b_name, "") or "") for b_name, r_name in field_mapping.items()}


def compare(b_prime, r_rows):
    """
    Compare B' against R.

    Returns (only_in_b_prime, only_in_r, mismatches) — B' = R only when
    all three are empty.
    """
    b_index = {row_key(row): row for row in b_prime}
    r_index = {row_key(row): row for row in r_rows}

    only_in_b_prime = [key for key in b_index if key not in r_index]
    only_in_r = [key for key in r_index if key not in b_index]

    mismatches = []
    for key in b_index.keys() & r_index.keys():
        differences = {
            field: (b_index[key].get(field), r_index[key].get(field))
            for field in b_index[key].keys() | r_index[key].keys()
            if _canonical_value(field, b_index[key].get(field)) != _canonical_value(field, r_index[key].get(field))
        }
        if differences:
            mismatches.append({"key": key, "diffs": differences})

    return only_in_b_prime, only_in_r, mismatches
