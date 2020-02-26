from market.etrade.common import ENV_MODE

import pprint

env_mode = ENV_MODE.ENV_PROD

import market.etrade.auth
session = market.etrade.auth.get_session(env_mode)


import market.etrade.account.positions
account = market.etrade.account.positions.Accounts(session, env_mode)

import market.etrade.sell.sell_all
sell = market.etrade.sell.sell_all.Sell(session, env_mode)
sell_response = sell.sell_all()
pprint.pprint(sell_response)
