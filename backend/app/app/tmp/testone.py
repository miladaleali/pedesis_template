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
from pedesis.tasks_manager import manager
from pedesis.station import Station

import pandas_ta as pdt
from datetime import datetime
from scalp.router import settings
from pedesis.components.data.sources.models import OhlcvDataRequest
from pedesis.shortcuts import get_data_handler

end = datetime.now().timestamp()

from scalp.router import BTCUSDT, gen1 as generator, ETHUSDT

station = Station()
station.start_all_public_components()
btc = BTCUSDT()
# eth = ETHUSDT()
generator.add_symbol(btc)
if generator.is_new():
    print('it is new')
    generator.create()

from pedesis.components.signal_optimizer.templates import NormalTolerance

nt = NormalTolerance()
nt.add_generators_channels(set([generator.get_channel()]))
nt.add_symbol(btc)
if nt.is_new():
    print('it is new')
    nt.create()

generator.init_quantify()
generator.signal_analysis_base_params = generator.settings.get_signal_base_params()

def make_signal(generator, timestamp: float, instant_price: float):
    from pedesis.components.signal_generator.models import Signal
    sig = generator.signal_analysis_base_params
    quality = generator.quality
    update = dict(
        timestamp=timestamp,
        quality=quality,
        instant_price=instant_price,
    )
    sig.update(**update)
    signal = Signal(**sig)
    # signal.add_to_db()
    return signal

from pedesis.components.signal_generator.models import AnalysisSignal
# sig = make_signal(multi, 1663463400000, 19408)
sig = AnalysisSignal.get(id=2).get_pydantic_model()
nt.signal_pool.add(sig)
from pedesis.components.signal_optimizer.events import register_signal_to_optimizer
# register_signal_to_optimizer(sig, nt.settings.dbid)
nt.timestamp = sig.timestamp

opt_sig = nt.make_signal()
