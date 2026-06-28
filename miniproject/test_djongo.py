import os
import django
from bson import ObjectId
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniproject.settings')
django.setup()

from django.db.models.fields import AutoField, BigAutoField

def custom_get_prep_value(self, value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return value

AutoField.get_prep_value = custom_get_prep_value
BigAutoField.get_prep_value = custom_get_prep_value

from django.contrib.auth.models import User, update_last_login

try:
    u = User.objects.create_user('testuser5', 't5@test.com', 'testpass')
    update_last_login(None, u)
    print("SUCCESS!")
except Exception as e:
    import traceback
    traceback.print_exc()
