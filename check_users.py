import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

print("Users and their groups:")
for user in User.objects.all():
    groups = list(user.groups.values_list('name', flat=True))
    print(f"User: {user.username}, Groups: {groups}, Superuser: {user.is_superuser}")

print("\nAvailable Groups:")
for group in Group.objects.all():
    print(f"Group: {group.name}")
