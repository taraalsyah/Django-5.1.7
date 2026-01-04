from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

#how to run this script:
# python manage.py shell < mywebsite/add_user_to_group.py


# Get the user model dynamically
User = get_user_model()

# Get the user and the group
user = User.objects.get(username='taraicode')
admin_group = Group.objects.get(name='Admin')

# Add user to Admin group
user.groups.add(admin_group)
user.save()