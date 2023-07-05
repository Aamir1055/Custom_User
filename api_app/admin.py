from django.contrib import admin

# Register your models here.
from api_app.models import CustomUser, UserDetails

admin.site.register(CustomUser)
admin.site.register(UserDetails)
