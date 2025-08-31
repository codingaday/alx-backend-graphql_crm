
from .celery import app as celery_app

default_app_config = "crm.apps.CrmConfig"


__all__ = ('celery_app',)
