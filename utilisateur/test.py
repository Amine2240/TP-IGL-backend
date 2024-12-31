import os
import sys

# Add the project directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Now set DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IGLBackend.settings')

from django.conf import settings
from django.contrib.auth.hashers import make_password

password = 'nazimaouni2'
hashed_password = make_password(password)
print(hashed_password)
