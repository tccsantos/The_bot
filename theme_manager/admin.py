from django.contrib import admin
from .models import User, Theme

# Register your models here.

admin.site.register(Theme)
admin.site.register(User)
