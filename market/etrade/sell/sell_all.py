import market.etrade.account.positions as market_positions
from market.etrade.common import order_preview_payload_format
import market.etrade.auth
import market.etrade.common
import os, datetime

_SELL_RETRIES = 3

_ETRADE_KEY = os.environ['ETRADE_KEY']
_ETRADE_SECRET = os.environ['ETRADE_SECRET']

class SellDryRun:
    def sell_all(self):
        print('(dry_run) selling all positions')

class Sell:
    def __init__(self, session, env_mode):
        self.session = session
        self.base_url = market.etrade.common.get_base_url(env_mode)
        self.market_positions = market_positions.Positions(session, env_mode)

    def _preview(self, account_id_key, position):
        url = self.base_url + "/v1/accounts/{accountIdKey}/orders/preview.json".format(accountIdKey=account_id_key)

        headers = {"Content-Type": "application/xml", "consumerKey": _ETRADE_KEY}

        symbol = position['symbolDescription']
        client_order_id = '{epoch}{symbol}'.format(epoch=str(int(datetime.datetime.now().timestamp())), symbol=symbol)
        payload = order_preview_payload_format.format(
            request_type='PreviewOrderRequest',
            preview_ids_block='',
            client_order_id=client_order_id,
            order_action="SELL",
            price_type='MARKET',
            limit_price='None',
            order_term='GOOD_UNTIL_CANCEL',
            quantity_type='QUANTITY',
            quantity=str(position['quantity']),
            symbol=symbol
        )

        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        return response.json(), client_order_id

    def get_preview_ids_xml(self, preview_js):
        preview_order_response = preview_js['PreviewOrderResponse']
        ids = '\n'.join(list(map(lambda pi: '<previewId>' + str(pi['previewId']) + '/<previewId>', preview_order_response['PreviewIds'])))
        return '<PreviewIds>' + ids + '</PreviewIds>'

    def _sell(self, account_id_key, position):
        preview_js, client_order_id = self._preview(account_id_key, position)
        preview_ids_xml = self.get_preview_ids_xml(preview_js)

        url = self.base_url + "/v1/accounts/{accountIdKey}/orders/place.json".format(accountIdKey=account_id_key)

        headers = {"Content-Type": "application/xml", "consumerKey": _ETRADE_KEY}

        symbol = position['symbolDescription']
        client_order_id = '{epoch}{symbol}'.format(epoch=str(int(datetime.datetime.now().timestamp())), symbol=symbol)
        payload = order_preview_payload_format.format(
            request_type='PlaceOrderRequest',
            preview_ids_block=preview_ids_xml,
            client_order_id=client_order_id,
            order_action="SELL",
            price_type='MARKET',
            limit_price='None',
            order_term='GOOD_UNTIL_CANCEL',
            quantity_type='ALL_I_OWN',
            quantity='',
            symbol=symbol
        )

        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        return response.json()

    def sell_all(self):
        positions = self.market_positions.get()
        print('selling {n} positions'.format(n=len(positions)))

        responses = []
        for account_id_key, account_positions in positions.items():
            print('selling a position for account: {account_id_key}'.format(account_id_key=account_id_key))
            if not account_positions: continue
            for i, position in enumerate(account_positions[0]):
                print('selling a position {i} for out of total {n}'.format(i=i, n=len(account_positions[0])))
                if position['positionType'] != 'LONG': continue;
                response = self._sell(account_id_key, position)
                responses.append(response)
        return responses
