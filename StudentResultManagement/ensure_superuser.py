import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentResultManagement.settings')
django.setup()

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    if created:
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' updated successfully.")
else:
    print("Superuser creation skipped: DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set.")
