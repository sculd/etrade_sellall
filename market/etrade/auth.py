from __future__ import print_function
import webbrowser
import os
from rauth import OAuth1Service

_ETRADE_KEY = os.environ['ETRADE_KEY']
_ETRADE_SECRET = os.environ['ETRADE_SECRET']

import market.etrade.common

def get_session(env_mode):
    base_rul = market.etrade.common.get_base_url(env_mode)
    etrade = OAuth1Service(
        name="etrade",
        consumer_key=_ETRADE_KEY,
        consumer_secret=_ETRADE_SECRET,
        request_token_url=base_rul + "/oauth/request_token",
        access_token_url=base_rul + "/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url=base_rul)

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a text code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter text code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})

    return session
