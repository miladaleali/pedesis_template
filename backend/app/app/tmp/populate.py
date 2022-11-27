# %%
symbols = [
    'BTCUSDT',
    'ETHUSDT',
    'ADAUSDT',
    'XRPUSDT',
    'DOTUSDT',
    'DOGEUSDT',
    'FILUSDT',
    'SOLUSDT',
]

timeframes = [
    '1d',
    '1m',
    '1h',
    '15m',
    '4h',
    '30m',
    '2h',
    '6h',
    '12h',
    '1w',
    '1M',
    '5m'
]

import nest_asyncio
nest_asyncio.apply()
from datetime import datetime

end = datetime.now().timestamp()

import backend.app.app.pretest as mock

# %%
station = mock.get_station()
# %%
btc = mock.get_btc_symbol()
generator = mock.get_generator(symbol=btc, back_populate=False)
optimizer = mock.get_optimizer(symbol=btc, generator=generator)
publisher = mock.get_publisher(symbol=btc, optimizer=optimizer)
# %%
# sig = mock.make_signal(
#     generator=generator,
#     timestamp=1665243300000,
#     instant_price=19300,
# ).add_to_db()
# %%
mock.add_signal_to_optimizer(optimizer=optimizer, signal_id=4)
srl = mock.get_srl_calculator(btc)
# %%
opt_sig = optimizer.make_signal()
# %%
pub_sig = publisher.make_signal(opt_sig)
pub_sig
# %%
import asyncio  

asyncio.run(pub_sig.open_position_caring())
# %%
from pedesis.components.data.tasks.data import (
    run_live_pub_ticker_stream_data_task,
    run_ticker_stream_data_task,
    run_stream_data_task
)
async def test_stream_data(signal, stream_func):
    from pedesis.shortcuts import get_data_handler
    from pedesis.components.data.sources.models import PriceTickerDataRequest
    from pedesis.components.pubsub.maker import create_redis_pubsub
    dhp = signal.get_engine().get_data_handler_params()
    dh = get_data_handler(**dhp)
    req = PriceTickerDataRequest(symbol=signal.symbol)
    req.localize_request(dh)
    req.stream_channel = req.signature(dh.signature())
    if not req.base_data_cache_uid:
        req.base_data_cache_uid = dh.make_data_store_cache_uid(req)
    stm = dh.source.ws.get_stream_data_model(req)
    return await stream_func(stm)

# %%

def load_okx_account(demo=False):
    from ccxt.async_support import okx
    import backend.app.app.apis as apis
    if demo:
        br = okx({
            'apiKey': apis.DemoApiKey,
            'secret': apis.DemoApiSecret,
            'password': apis.DemoPassphrase,
        })
        br.set_sandbox_mode(True)
        br.aiohttp_proxy = "http://Zm0ExKmqUR:SCl64J5AUX@185.173.107.66:26737"
        return br
    return okx(config={
        'apiKey': apis.ApiKey,
        'secret': apis.ApiSecret,
        'password': apis.Passphrase,
    })

# %%
def load_contract():
    from pedesis.components.contract.models import ContractModel
    return ContractModel.get(id=1)

# %%
def create_contract_manager(station):
    from pedesis.components.contract.controller import ContractManager
    station.start_all_engines()
    eng = station.running_engines['scalp'].engine()
    eng.generators = {1}
    eng.optimizers = {2}
    eng.publishers = {3}
    station.start_all_contracts()
    cont = load_contract().get_pydantic_model()
    return ContractManager(cont, station._engine_clusters['scalp'])

# %%
cm = create_contract_manager(station)
# %%
from pedesis.components.contract import events

# %%
gp_cache_uid = mock.prepare_generic_position(
    generic_position_id=2,
    main_price_1=20900,
    # main_price_2=21200,
    # tp_price_1=22000,
    # tp_price_2=23000,
    # sl_price_1=19500,
    # sl_price_2=18700,
    save_it=True,
)
data = {'cache_uid': gp_cache_uid}  # generic position
# %%
cid, data = events.get_create_position_notice(cm, data)
# %%
# def demo_position():
#     from pedesis.components.contract.models import Position
#     import functools
#     class DemoPosition(Position):
#         @functools.lru_cache
#         def get_broker(self):
#             br = super().get_broker()
#             br.set_sandbox_mode(True)
#             return br
#     return DemoPosition

# %%
from backend.app.app.apis import DemoPosition
def test_contrct_open_position_caring(
    contract_cache_id: str,
    position_data: dict,
):
    from pedesis.components.contract.tasks.position import open_position_caring
    from pedesis.utils import make_uid
    import asyncio
    asyncio.run(
        open_position_caring(
            contract_cache_uid=contract_cache_id,
            position_data=position_data,
            position_model=DemoPosition,
            position_task_id=make_uid()
        )
    )

# %%
def create_position(cont_cid: str, pos_data: dict, pos_model=DemoPosition):
    from pedesis.shortcuts import get_current_cache
    gp = get_current_cache().get(pos_data['cache_uid'])
    return pos_model(
        task_id='test',
        generic_position=gp,
        contract_cache_uid=cont_cid,
        margin_portion=pos_data['margin'],
        leverage=pos_data['leverage'],
        risk=pos_data['risk']
    )
# %%
from pedesis.components.contract.models import Position, Order
def load_position(_id: int = 27) -> Position:
    from pedesis.components.contract.models import OpenPositionModel
    import pickle
    return pickle.loads(OpenPositionModel.get('position', id=_id))

pos = load_position(45)
# pos = create_position(cid, data)
# %%
import asyncio
asyncio.run(pos.send_batch_orders(pos.total_orders.main, 'main'))
# %%
def test_is_open(position: Position):
    try:
        print(asyncio.run(position.is_position_open()))
    except KeyboardInterrupt:
        pass

# %%
test_is_open(pos)
# %%
asyncio.run(pos.send_all_exit_orders())
# %%
asyncio.run(pos.check_all_enter_order_filled(False))
# %%
asyncio.run(pos.update_exit_released_orders())
# %%
asyncio.run(pos.this_exit_order_line_filled('sl'))
# %%
