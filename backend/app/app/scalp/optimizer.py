from pedesis.components import signal_optimizer as optimizer
from app.scalp.optimizer_settings import (
    HighRiskSettings
)

# The task of this class is to form the signal equation. which is a 
# combination of direct, confirmative and adjuster signals. that equation is:
# adjuster * (direct + confirmative)
# When a direct signal is received, this equation is formed and the quality of the signals is 
# included in this equation (if there are other signals, otherwise the adjuster is 1 and the confirmative is 0).

# To create a new class, we just need to write a new configuration and add it to the base class.

class HighRiskOptimizer(optimizer.controller.Optimizer):
    SETTINGS = HighRiskSettings
