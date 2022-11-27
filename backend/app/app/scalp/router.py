from typing import List
from pedesis.components.signal_generator.controller import Generator
from pedesis.components.signal_optimizer.controller import Optimizer
from pedesis.components.signal_publisher.controller import Publisher

import pedesis.components.symbol_router as router
from pedesis.components.stream_processor.models import CustomSetting  # noqa
from pedesis.components.signal_generator.models import DataHandlerAssembly  # noqa
from pedesis.components.symbol_router.maker import generator_assemble  # noqa
from pedesis.shortcuts import get_source  # noqa
from . import generator as gen  # noqa
from . import optimizer as opt  # noqa
from . import publisher as pub  # noqa
from . import settings


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

gen1 = generator_assemble(
    raw_generator=gen.IchimokuUpTrendDT,
    data_handler=[lower_handler, upper_handler]
)

class BaseSymbol(router.SymbolRouter):
    """ this is a base class for each symbol that will be add in the engine to  """
    ENGINE_SETTINGS = settings
    ENGINE_PROPERTY = settings.ENGINE_PROPERTY
    ENGINE_RUN_CONFIGS = {
        'mode': settings.ENGINE_RUN_MODE,
        'start_datetime': settings.ENGINE_START_BACKTEST_DATETIME,
        'end_datetime': settings.ENGINE_END_BACKTEST_DATETIME,
    }
    SRL_TIMEFRAMES = settings.SRL_TIMEFRAMES
    # FIXME: srl setting is in setting file then we can use it directly, then refactor this.
    SRL_CALCULATORS = settings.INSTALLED_SRLS  # name of calculators in srl_calculator/calculators/...
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
