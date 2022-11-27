from datetime import datetime
import pandas as pd
import numpy as np
from pedesis.components.srl_calculator.calculators.utils import (
    DataSettings,
    CalculatorTimeFrameSettings as CTSettings
)

name = str(__file__)

_START_TIME = datetime(2020, 1, 1).timestamp() * 1000

data_settings = DataSettings(start_time=_START_TIME)

CONFIGS = {
    '5m': CTSettings(
        timeframe='5m', 
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        first_std_srl=0.02,
        other=dict(
            period=20
        ),
    ),
    '15m': CTSettings(
        timeframe='15m',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=20
        ),
    ),
    '30m': CTSettings(
        timeframe='30m',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=20
        ),
    ),
    '1h': CTSettings(
        timeframe='1h',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=15
        ),
    ),
    '2h': CTSettings(
        timeframe='2h',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=10
        ),
    ),
    '4h': CTSettings(
        timeframe='4h',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=10
        ),
    ),
    '6h': CTSettings(
        timeframe='6h',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=10
        ),
    ),
    '12h': CTSettings(
        timeframe='12h',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=10
        ),
    ),
    '3d': CTSettings(
        timeframe='3d',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=5
        ),
    ),
    '1w': CTSettings(
        timeframe='1w',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=3
        ),
    ),
    '1M': CTSettings(
        timeframe='1M',
        srlevel_std_multiplier=1.05,
        data_settings=data_settings,
        other=dict(
            period=2
        ),
    ),
}

# NOTE: this func must be named calculate.
def calculate(df: pd.DataFrame, setting: CTSettings) -> pd.DataFrame:
    """Indicate bearish and bullish fractal patterns using shifted Series.

    :param df: OHLC data
    :param period: number of lower (or higher) points on each side of a high (or low)
    :return: pd.DataFrame (bearish, bullish) where True marks a fractal pattern
    """
    period = setting.other['period']
    periods = [p for p in range(-period, period + 1) if p != 0]  # default [-2, -1, 1, 2]

    highs = [df['high'] > df['high'].shift(p) for p in periods]
    bears = pd.Series(np.logical_and.reduce(highs), index=df.index)

    lows = [df['low'] < df['low'].shift(p) for p in periods]
    bulls = pd.Series(np.logical_and.reduce(lows), index=df.index)

    return df[bears | bulls]
