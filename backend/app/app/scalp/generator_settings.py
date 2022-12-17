from pedesis.components.signal_generator.templates import base_setting as base

# ==============================================================================
# ==============================  IchimokuUpTrendDT Start ======================
# ==============================================================================

# Settings of each generator includes three parts, which are input, logic and output.
# In the logic section, indicators are defined. In the input section, the characteristics
# of the input data to the generator are defined, and in the output section, the
# characteristics of the signal produced by the generator are defined.

# Each of the settings can be expressed in two ways, single or layered. For example,
# if we want to use two data sources for input settings, we should use layered input settings.
# Each layered input settigns is a layer composed of 2 or more input settings.

# If layer settings are used, for each layer that is defined in the input section, 
# a layer with the same name must be defined in the logic section.

# ==============================  Logic Start ==================================
# In the logic section, indicators are calculated
class IchiLowerTM(base.GeneratorLogicSetting):
    template_name: str = 'IchimokuUpTrendDT'  # name of the generator class
    # Next, we define the settings we want to use.
    kijun: int = 9  # kijun sen period that want to use in ichimoku indicator
    tenkan: int = 26
    senkou_b: int = 52
    trend_source: str = 'close'  # source of the trend indicator
    trend: int = 100  # period of the trend indicator

    # In below attribute, we write the names of the indicators that we want to calculate 
    # in this logic. Note that these names should not be the same as the names of the 
    # indicators of other layers in this logic setting.

    # Another point, the name of the indicators must be the same as the attributes we 
    # have defined as indicators inside the generator class.
    all_indicators: base.List[str] = [
        'ichimoku',
        'lower_trend'
    ]

    @base.cache_indicator
    def mono_calculate(
        self, 
        datas: base.pd.DataFrame,
        indicator_cache_stores: base.Dict[str, str],
        indi_name: str
    ) -> None:
        # in this calculate method, datas is lower data layer.
        match indi_name:
            case 'ichimoku':
                return base.pdt.ichimoku(
                    high=datas['high'],
                    low=datas['low'],
                    close=datas['close'],
                    tenkan=self.tenkan,
                    kijun=self.kijun,
                    senkou=self.senkou_b,
                )
            case 'lower_trend':
                return base.calculate_ema(
                    data=datas,
                    source=self.trend_source,
                    period=self.trend
                )

class IchiUpperTM(base.GeneratorLogicSetting):
    template_name: str = 'IchimokuUpTrendDT'
    trend_source: str = 'close'
    trend: int = 100
    all_indicators: base.List[str] = [
        'upper_trend',
    ]

    @base.cache_indicator
    def mono_calculate(
        self, 
        datas: base.pd.DataFrame,
        indicator_cache_stores: base.Dict[str, str],
        indi_name: str
    ) -> None:
        # in this calculate method, datas is upper data layer.
        return base.calculate_ema(datas, self.trend_source, self.trend)

class IchiLayeredLogic(base.LayerGeneratorLogicSetting):
    # Layered logic is a model where each layer is defined as an attribute whose name 
    # is the same as the name defined in the layered data.
    template_name: str = 'IchimonkuUpTrendDT'
    lower: IchiLowerTM = IchiLowerTM()
    upper: IchiUpperTM = IchiUpperTM()

# ==============================  Logic End ==================================

# ==============================  Input Start ================================
# Every data we intend to receive has a request that we must define in this section.
# in this example, we want to receive Ohlcv datas for two different timeframes.
lower_req = base.OhlcvStreamDataRequest(timeframe='5m')
upper_req = base.OhlcvStreamDataRequest(timeframe='1d')

class IchiLowerInput(base.GeneratorInputSetting):
    # Each data setting requires a request that must be set. The rest of this model
    # is automatically set when the program is run.
    request: base.OhlcvStreamDataRequest = lower_req

class IchiUpperInput(base.GeneratorInputSetting):
    request: base.OhlcvStreamDataRequest = upper_req

class IchiLayeredInput(base.LayerGeneratorInputSetting):
    # As mentioned in the logic section, when layer settings are used, 
    # the names of the layer in the data and logic must be the same.
    template_name: str = 'IchimokuUpTrendDT'
    lower: IchiLowerInput = IchiLowerInput()
    upper: IchiUpperInput = IchiUpperInput()

# ==============================  Input End ==================================

# ==============================  Output Start ===============================
# The output setting only specifies the characteristics of the signal coming out of this generator.
output_settings = base.GeneratorOutputSetting(
    signal_type=base.SignalType.Long,  # type of signal, Long or Short
    analysis_style=base.AnalysisStyle.Technical,  # style of analysis, Technical, Fundamental, Sentimental or OnChain
    optimizer_tag=base.OptimizerTag.Direct,  # this tag is used to determine the type of signal in optimizer.
    consumption_pattern=base.ConsumptionPattern.Disposable,  # this tag is used to determine weather the signal is disposable or not.
    signal_mode=base.SignalMode.Analysis,  # this tag is used to determine the mode of signal, Analysis or Trade.
    expire_configs=base.ExpireConfigs(  # this config is used to determine the expire time of signal.
        configs={
            'timedelta': 24 * 60  # one day
        }
    )
)

# ==============================  Output End =================================
ichi_logic = IchiLayeredLogic()

IchiSettings = base.GeneratorSettings.safe_creation(
    template_name='IchiUpTrendDT',
    logic=ichi_logic,
    output=output_settings,
    input_=IchiLayeredInput()
)

# Just for some reason, this variable needs to be initialized again.
# IchiSettings.logic = ichi_logic

# ==============================  IchimokuUpTrendDT End  =======================
# ==============================================================================
