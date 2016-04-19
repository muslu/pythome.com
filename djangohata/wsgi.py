import os

import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/muslu/django/')
sys.path.append('/home/muslu/django/djangohata/')
sys.path.append('/home/muslu/django/djangohata/djangohata/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangohata.settings")

application = get_wsgi_application()
