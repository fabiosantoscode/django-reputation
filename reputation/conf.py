"""
application configuration for django-reputation
"""

from appconf import AppConf


class ReputationConf(AppConf):
    MAX_GAIN_PER_DAY = 100
    MAX_LOSS_PER_DAY = 100
    SITECONF = "reputation_sites"
    PERMISSIONS = {}
    DIMENSIONS = {'CO': 'contributor'}

    class Meta:
        prefix = 'reputation'
        proxy = True


settings = ReputationConf()
