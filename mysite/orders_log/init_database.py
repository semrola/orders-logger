from django.contrib.auth.models import User

user = User.objects.create_user('sandi', 'sandi@gmail.com', 'sandi')
user.save()