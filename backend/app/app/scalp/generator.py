from typing import Tuple
import pandas as pd
from pedesis.components.signal_generator import templates as generators
from pedesis.components.signal_generator.controller import Generator
from pedesis.components.signal_generator.templates.base import speedy_cross
from . import generator_settings as gsettings  # noqa

# In this file, we define the generator classes, and inside the classes, we only 
# write the signal generation logic, and how the indicators are calculated are
# defined in the settings file.

class IchimokuUpTrendDT(Generator):
    EXPECTED_INVESTMENT_TIME = 1 * 60  # 1 hour
    TIMEFRAME: str = '5m'
    SETTINGS = gsettings.IchiSettings

    def __init__(self):
        super().__init__()

        # Next, we will define the indicators and use the same naming as we did in the settings here.
        # Here we only initiate the indicators, they are automatically set values at runtime.
        # indicators
        self.ichimoku: Tuple[pd.DataFrame] = None  # df1_columns(main indicator): ISA_9	ISB_26 ITS_9 IKS_26	ICS_26; df2_columns(future cloud): ISA_9 ISB_26
        self.trend: pd.Series = None

        # Below we define the data we have. If there are multiple data layers define data like this: ({layer_name}_data)
        # if there is only one data layer it is defined like this: main_data.
        # datas
        self.lower_data: pd.DataFrame = None
        self.upper_data: pd.DataFrame = None

    def up_trend(self) -> bool:
        # partial calc for calculate signal logic.
        # Higher time frame data is used to find out whether the overall situation is bullish or bearish.
        return self.upper_data.close.iloc[-1] >= self.trend.iloc[-1]

    def current_cloud_is_up(self) -> bool:
        # partial calc for calculate signal logic.
        return self.ichimoku[0].ISA_9.iloc[-1] >= self.ichimoku[0].ISB_26.iloc[-1]

    def cross_up_tenken_kijun(self) -> bool:
        # partial calc for calculate signal logic.
        ichi = self.ichimoku[0]
        return speedy_cross(ichi.ITS_9, ichi.IKS_26)

    def future_cloud_is_up_flat(self) -> bool:
        # partial calc for calculate signal logic.
        ichi = self.ichimoku[1]
        return ichi.ISA_9.iloc[-1] >= ichi.ISB_26.iloc[-1]

    def signal_logic(self) -> bool:
        # In this function, we write the logic that we want to check to generate a signal if it occurs.
        if (
            self.up_trend() and
            self.future_cloud_is_up_flat() and
            self.current_cloud_is_up() and
            self.cross_up_tenken_kijun()
        ):
            return True
        return False
