"""
WSGI config for enHuecoAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enHuecoAPIMain.settings")
sys.path.append('/home/acmdevelop/enHuecoAPI/enHuecoAPI/enHuecoAPIMain')
sys.path.append('/home/acmdevelop/enHuecoAPI/enHuecoAPI')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
