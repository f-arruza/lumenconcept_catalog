import os
from django.core.wsgi import get_wsgi_application
from catalog.tasks import offer_verification

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lumenconcept_catalog.settings")

application = get_wsgi_application()

# offer_verification()
