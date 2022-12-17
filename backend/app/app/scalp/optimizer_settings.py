from pedesis.components.signal_optimizer.templates import base_setting as base

# =============================================================
# ==================== High Risk Optimizer ====================
# =============================================================

# Currently, the only setting available for this section is the threshold,
# which accepts a number between 0 and 1.
logic = base.OptimizerLogicSetting(
    template_name='HighRiskOptimizer',
    threshold=0.1,  # Threshold is a criterion to check the score of the signal equation, whether the signal can be propagated or not
)

HighRiskSettings = base.OptimizerSettings.safe_creation(
    template_name='HighRiskOptimizer',
    logic=logic,
)
