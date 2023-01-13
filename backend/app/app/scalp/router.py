from typing import List
from pedesis.components.signal_generator.controller import Generator
from pedesis.components.signal_optimizer.controller import Optimizer
from pedesis.components.signal_publisher.controller import Publisher

import pedesis.components.symbol_router.controller as router
from pedesis.components.stream_processor.models import CustomSetting  # noqa
from pedesis.components.signal_generator.models import DataHandlerAssembly  # noqa
from pedesis.components.symbol_router.maker import generator_assemble  # noqa
from pedesis.shortcuts import get_source  # noqa
from . import generator as gen  # noqa
from . import optimizer as opt  # noqa
from . import publisher as pub  # noqa
from .settings import settings


# define frequently use variables in this section
_OKX_SRC_PATH = 'pedesis.components.broker.templates.okx'

# =============================================================================
# define source like below
okx = get_source(_OKX_SRC_PATH)

# define data_handler setting like below
lower_handler = DataHandlerAssembly(
    data_source=okx.dbid,
    section='lower',
    market='future'
)
upper_handler = DataHandlerAssembly(
    data_source=okx.dbid,
    section='upper',
    market='future'
)

# gen1 = generator_assemble(
#     gen.generators.MacdRsiOs,
#     data_handler=[lower_handler],
# )

gen1 = gen.IchimokuUpTrendDT(data_handler=[lower_handler, upper_handler])

class BaseSymbol(router.SymbolRouter):
    """ this is a base class for each symbol that will be add in the engine to  """
    ENGINE_SETTINGS = settings
    ENGINE_PROPERTY = settings.engine_property
    ENGINE_RUN_CONFIGS = {
        'mode': settings.run_mode,
        'start_datetime': settings.backtest_start_datetime,
        'end_datetime': settings.backtest_end_datetime,
    }
    SRL_TIMEFRAMES = settings.srl_timeframes
    # FIXME: srl setting is in setting file then we can use it directly, then refactor this.
    SRL_CALCULATORS = settings.installed_srls  # name of calculators in srl_calculator/calculators/...
    GENERATORS: List[Generator] = [  # add general generator object in this section
        gen1,
    ]
    OPTIMIZERS: List[Optimizer] = [  # add general optimizer object in this section
        opt.HighRiskOptimizer()
    ]
    PUBLISHERS: List[Publisher] = [  # add general publisher object in this section
        pub.SharpPublisher()
    ]


# define customize settings like below
# gen1_btc = gen1.customize_settings(
#     CustomSetting(
#         component='input',
#         customize={
#             'market': 'spot'
#         }
#     ),
#     CustomSetting(
#         component='logic',
#         customize={
#             'kijun': 15
#         }
#     )
# )

# define trading Symbol like below
class BTCUSDT(BaseSymbol):
    # define custom generators like below:
    # CUSTOM_GENERATORS: List[Generator] = [gen1_btc]
    pass

class ETHUSDT(BaseSymbol):
    pass


class DOGEUSDT(BaseSymbol):
    pass
