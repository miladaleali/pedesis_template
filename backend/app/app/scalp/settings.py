from datetime import datetime

from pedesis.components.signal_engine import models
from pedesis.conf import EngineSettings

class Settings(EngineSettings):
    run_mode: str = 'live'

    name: str = 'scalp'
    folder_name: str = 'scalp'
    mode: models.EngineMode  = models.EngineMode.Scalp
    native_broker: str = 'pedesis.components.broker.templates.okx'
    market: str = models.DataType.Future

    backtest_start_datetime: str = '2022-03-01 00:00:00'
    back_populate_start_datetime: float = datetime(2020, 1, 1).timestamp()

    installed_data_sources: dict[str, str] = {
        'okx': 'pedesis.components.broker.templates.okx',
    }
    installed_srls: list[str] = [
        'scalp.srls.williams'
    ]
    srl_timeframes: list[str] = [
        '5m',
        '15m',
        '30m',
        '1h',
        '2h',
        '4h',
        '6h',
        '12h',
        '1d',
        '3d',
        '1w',
        '1M',
    ]

    installed_symbols: list[str] = [  # write name of trading symbol that want to use
        'BTCUSDT',
        'ETHUSDT',
        'DOGEUSDT',
    ]
