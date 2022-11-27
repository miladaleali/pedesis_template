from pedesis.components.signal_publisher.templates import base_setting as base

# =============================================================
# ==================== Sharp Publisher ========================
# =============================================================

sharp_enterance_limit_adjuster = {
    '0-40': 0.45,
    '40-80': 0.3,
    '80-90': 0.2,
    '90-101': 0.1,
}

sharp_logic = base.PublisherLogicSetting(
    template_name='SharpPublisher',
    risk_tolerance_pct=4,
    raw_enterance_limit_adjuster=sharp_enterance_limit_adjuster,
    signal_perfect_score=0.85,
    support_srlevel_quality=100,
    resistance_srlevel_quality=100,
    stop_loss_orders_portion=(30, 40, 30),
    take_profit_orders_portion=(20, 60, 20),
)

SharpPublisherSettings = base.PublisherSettings(
    template_name='SharpPublisher',
    logic=sharp_logic,
)

SharpPublisherSettings.logic = sharp_logic
