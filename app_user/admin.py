from django.contrib import admin

# Register your models here.
from app_user.models import User, CredentialsModel

admin.site.register(User)
admin.site.register(CredentialsModel)

