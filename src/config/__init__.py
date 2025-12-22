import os

from .development_conf import DevelopmentConfig
from .production_conf import ProductionConfig

ENVIRONMENT = os.getenv("ENVIRONMENT") or "prod"

configs = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}

settings: DevelopmentConfig | ProductionConfig = configs[ENVIRONMENT]()
