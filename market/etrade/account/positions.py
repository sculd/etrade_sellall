import logging
from logging.handlers import RotatingFileHandler
from market.etrade.common import SANDBOX_BASE_URL
import market.etrade.common
from collections import defaultdict

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

# https://api.etrade.com/v1/accounts/{accountIdKey}/portfolio

class Accounts:
    def __init__(self, session, env_mode):
        self.session = session
        self.base_url = market.etrade.common.get_base_url(env_mode)

    def get(self):
        url = self.base_url + "/v1/accounts/list.json"

        response = self.session.get(url)
        if response is not None and response.status_code == 200:
            js = response.json()
            if "AccountListResponse" not in js:
                return []
            if "Accounts" not in js["AccountListResponse"]:
                return []
            if "Account" not in js["AccountListResponse"]["Accounts"]:
                return []
            return js["AccountListResponse"]["Accounts"]["Account"]
        else:
            return []

    def get_account_id_key(self):
        acc = self.get()
        for a in acc:
            if a['accountMode'] == 'CASH':
                return a['accountIdKey']
        return ''

class Positions:
    def __init__(self, session, env_mode):
        self.session = session
        self.base_url = market.etrade.common.get_base_url(env_mode)
        self.accounts = Accounts(session, env_mode)

    def get(self):
        accounts = self.accounts.get()

        res = defaultdict(list)
        for account in accounts:
            if 'accountIdKey' not in account:
                continue

            accountIdKey = account['accountIdKey']
            url = self.base_url + "/v1/accounts/{accountIdKey}/portfolio.json".format(accountIdKey=accountIdKey)
            response = self.session.get(url)

            if response is not None and response.status_code == 200:
                js = response.json()
                if "PortfolioResponse" not in js:
                    continue
                if "AccountPortfolio" not in js["PortfolioResponse"]:
                    continue
                for portfolio in js["PortfolioResponse"]["AccountPortfolio"]:
                    if "Position" not in portfolio:
                        continue
                    res[accountIdKey].append(portfolio["Position"])

        return res

