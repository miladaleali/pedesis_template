
def get_station():
    from pedesis.station.controller import Station
    station = Station()
    station.start_all_public_components()
    return station

def get_btc_symbol():
    from scalp.router import BTCUSDT
    return BTCUSDT()

def get_generator(
    symbol,
    back_populate: bool = False,
):
    from scalp.router import gen1 as generator
    import asyncio
    generator.add_symbol(symbol)
    if generator.is_new():
        print('it is new')
        generator.create()
    generator.init_quantify()
    generator.signal_analysis_base_params = generator.settings.get_signal_base_params()
    if back_populate:
        asyncio.run(generator.back_populate_setup())
    return generator

def get_optimizer(
    symbol,
    generator,
):
    from pedesis.components.signal_optimizer.templates import NormalTolerance
    nt = NormalTolerance()
    nt.add_generators_channels(set([generator.get_channel()]))
    nt.add_symbol(symbol)
    if nt.is_new():
        print('it is new')
        nt.create()
    return nt

def get_publisher(
    symbol,
    optimizer,
):
    from pedesis.components.signal_publisher.templates import MeduimRisk
    mr = MeduimRisk()
    mr.add_optimizers_channels(set([optimizer.get_channel()]))
    mr.add_symbol(symbol)
    if mr.is_new():
        print('it is new')
        mr.create()
    return mr

def make_signal(
    generator,
    timestamp: float,
    instant_price: float
):
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

# sig = make_signal(multi, 1663463400000, 19408)
def add_signal_to_optimizer(optimizer, signal=None, signal_id=None):
    from pedesis.components.signal_generator.models import AnalysisSignal
    from pedesis.components.signal_optimizer.events import register_signal_to_optimizer
    reg = True
    if not signal:
        reg = False
        signal = AnalysisSignal.get(id=signal_id).get_pydantic_model()
    optimizer.signal_pool.add(signal)
    if reg:
        register_signal_to_optimizer(signal, optimizer.settings.dbid)
    optimizer.timestamp = signal.timestamp

def get_srls_calculator(symbol):
    from scalp.settings import ENGINE_PROPERTY, SRL_TIMEFRAMES
    from pedesis.components.srl_calculator.maker import _mono_setup_srls

    _mono_setup_srls(
        engine=ENGINE_PROPERTY,
        symbol=symbol.__name__,
        timeframes=symbol.SRL_TIMEFRAMES,
        calculators=symbol.SRL_CALCULATORS,
    )

def get_srl_calculator(
    symbol,
    srls_id: int = 1,
    timeframe: str = "15m",
):
    from pedesis.components.srl_calculator.controller import SRL
    from pedesis.components.srl_calculator.models import SRLConfigs, SRLsModel
    if not SRLsModel.get(id=srls_id):
        from scalp.settings import ENGINE_PROPERTY
        from pedesis.components.data.models import UniSymbol
        import json
        sym_id = UniSymbol.get(symbol=symbol.__class__.__name__).id
        tm = json.dumps(symbol.SRL_TIMEFRAMES)
        calcs = json.dumps(symbol.SRL_CALCULATORS)
        eng_sig = ENGINE_PROPERTY.signature()
        if (
            srls_id := SRLsModel.get(
                'id',
                signal_engine_signature=eng_sig,
                uni_symbol_id=sym_id,
                timeframes=tm,
                calculators=calcs,
            )
        ) is None:
            srls = SRLsModel(
                signal_engine_signature=eng_sig,
                uni_symbol_id=sym_id,
                timeframes=tm,
                calculators=calcs,
            ).save()
            srls_id = srls.id
    conf = SRLConfigs(
        srls_id=srls_id,
        timeframe=timeframe,
        calculator=symbol.SRL_CALCULATORS[0],
    )
    return SRL(conf)

def prepare_generic_position(
    generic_position_id: int,
    main_price_1: float = None,
    main_price_2: float = None,
    tp_price_1: float = None,
    tp_price_2: float = None,
    sl_price_1: float = None,
    sl_price_2: float = None,
    save_it: bool = False,
    return_cache: bool = True,
):
    from pedesis.components.signal_publisher.models import (
        GenericPosition,
        GenericPositionModel
    )
    gpb = GenericPositionModel.get('generic_position', id=generic_position_id)
    gp = GenericPosition.from_pickle(gpb)
    if main_price_1:
        gp.initial_orders.main[0].price = main_price_1
    if main_price_2:
        gp.initial_orders.main[1].price = main_price_2
    if tp_price_1:
        gp.initial_orders.tp[0].price = tp_price_1
    if tp_price_2:
        gp.initial_orders.tp[1].price = tp_price_2
    if sl_price_1:
        gp.initial_orders.sl[0].price = sl_price_1
    if sl_price_2:
        gp.initial_orders.sl[1].price = sl_price_2
    if save_it:
        gp.asave()
    gp.cacheit()
    if return_cache:
        return gp.uid
    return gp
