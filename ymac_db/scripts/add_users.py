import sys

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

users = [
    ("bstjames", "bstjames@ymac.org.au", "Brooke", "St James"),
    ("amgibbs", "amgibbs@ymac.org.au", "Anna Marie", "Gibbs"),
]

for username, email, first_name, last_name in users:
    try:
        print 'Creating user {0}.'.format(username)
        user = User.objects.create_user(
            username=username,
            email=email,
            is_staff=True,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password("password123")
        user.save()

        assert authenticate(username=username, password="password123")
    except:
        print 'There was a problem creating the user: {0}.  Error: {1}.' \
            .format(username, sys.exc_info()[1])
