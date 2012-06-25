from django.core.management import setup_environ
import sys

sys.path.append('/var/wsgi/maiznet')
sys.path.append('/var/wsgi')

from maiznet import settings

setup_environ(settings)

from maiznet.register.models import Presence

wfile = open("/var/wsgi/maiznet/tools/ml/emails","w")
presence = Presence.objects.filter(talkings=1).all()
#presence = Presence.objects.all()

for p in presence :
	mail = p.user.email
	wfile.write(mail + "\n")
