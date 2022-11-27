from pedesis.components.signal_publisher.templates import base
from scalp.publisher_settings import (
    SharpPublisherSettings,
)


class SharpPublisher(base.Publisher):
    SETTINGS = SharpPublisherSettings
