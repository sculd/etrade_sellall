
order_preview_payload_format = """
           <{request_type}>
               <orderType>EQ</orderType>
               <clientOrderId>{client_order_id}</clientOrderId>
               {preview_ids_block}
               <Order>
                   <allOrNone>false</allOrNone>
                   <priceType>{price_type}</priceType>
                   <orderTerm>{order_term}</orderTerm>
                   <marketSession>REGULAR</marketSession>
                   <stopPrice></stopPrice>
                   <limitPrice>{limit_price}</limitPrice>
                   <Instrument>
                       <Product>
                           <securityType>EQ</securityType>
                           <symbol>{symbol}</symbol>
                       </Product>
                       <orderAction>{order_action}</orderAction>
                       <quantityType>{quantity_type}</quantityType>
                       <quantity>{quantity}</quantity>
                   </Instrument>
               </Order>
           </{request_type}>"""


from enum import Enum

class ENV_MODE(Enum):
    ENV_SANDBOX = 1
    ENV_PROD = 2

SANDBOX_BASE_URL = 'https://apisb.etrade.com'
PROD_BASE_URL = 'https://api.etrade.com'

def get_base_url(env_mode):
    if env_mode is ENV_MODE.ENV_SANDBOX:
        return SANDBOX_BASE_URL
    elif env_mode is ENV_MODE.ENV_PROD:
        return PROD_BASE_URL
    return SANDBOX_BASE_URL
