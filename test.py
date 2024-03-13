import gettext

try:
    gettext.find('django', 'django.mo')
    print("Gettext installed.")
except IOError:
    print("Gettext not installed or configuration error.")