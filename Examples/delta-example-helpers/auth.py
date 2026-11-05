"""OAuth1 request signing for Mastercard APIs, backed by a PKCS#12 certificate."""
import oauth1.authenticationutils as authenticationutils
from oauth1.signer import OAuthSigner
from requests.auth import AuthBase


class MCSigner(AuthBase):
    """A `requests`-compatible auth handler that OAuth1-signs outgoing requests."""

    def __init__(self, consumer_key, signing_key):
        self.signer = OAuthSigner(consumer_key, signing_key)

    def __call__(self, request):
        self.signer.sign_request(request.url, request)
        return request


def make_signer(consumer_key, p12_path, password):
    """Build an OAuth1 signer to pass as `auth=` in `requests` calls."""
    signing_key = authenticationutils.load_signing_key(p12_path, password)
    return MCSigner(consumer_key, signing_key)
