"""
Paginated BinLookup API helpers.

All requests go through `_request_with_retry`, which retries with
exponential backoff (1s, 2s, 4s, ...) on transient failures: HTTP 429/5xx
responses and network-level errors (timeouts, connection resets).
"""
import time
import requests

PAGE_SIZE = 10000        # max rows per page for /bin-ranges
DELTA_PAGE_SIZE = 1000   # max rows per page for the delta endpoint

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _request_with_retry(method, url, params, signer, headers, retries=3):
    """Call `method(url, ...)`, retrying with exponential backoff on transient failures."""
    last_error = None
    for attempt in range(retries):
        try:
            response = method(url, params=params, auth=signer, headers=headers)
        except requests.exceptions.RequestException as exc:
            last_error = exc
        else:
            if response.status_code == 200:
                return response.json()
            if response.status_code not in RETRYABLE_STATUS_CODES:
                raise RuntimeError(f"{url} failed: {response.status_code} {response.text[:300]}")
            last_error = RuntimeError(f"{url} returned {response.status_code}: {response.text[:300]}")

        if attempt < retries - 1:
            time.sleep(2 ** attempt)

    raise RuntimeError(f"{url} failed after {retries} retries: {last_error}")


def _get(url, params, signer, retries=3):
    """Send a GET request and return the parsed JSON body."""
    headers = {"Accept": "application/json"}
    return _request_with_retry(requests.get, url, params, signer, headers, retries)


def _post(url, params, signer, retries=3):
    """Send a POST request and return the parsed JSON body."""
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    return _request_with_retry(requests.post, url, params, signer, headers, retries)


def fetch_delta(base_url, snapshot_id, signer):
    """Page through /bin-ranges/deltas/snapshots/{snapshot_id} and return (items, delta_id)."""
    items, delta_id, page = [], None, 1
    while True:
        payload = _get(
            f"{base_url}/bin-ranges/deltas/snapshots/{snapshot_id}",
            {"page": page, "size": DELTA_PAGE_SIZE},
            signer,
        )
        delta_id = payload.get("id", delta_id)
        items.extend(payload.get("items", []))
        if payload.get("currentPageNumber", page) >= payload.get("totalPages", page):
            break
        page += 1
    return items, delta_id


def download_snapshot_r(base_url, signer):
    """Page through POST /bin-ranges and return the full list of current BIN range items."""
    items, page = [], 1
    while True:
        payload = _post(f"{base_url}/bin-ranges", {"page": page, "size": PAGE_SIZE}, signer)
        items.extend(payload.get("items", []))
        if payload.get("currentPageNumber", page) >= payload.get("totalPages", page):
            break
        page += 1
    return items
