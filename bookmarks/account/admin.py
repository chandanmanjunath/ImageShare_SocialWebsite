from django.contrib import admin
# Register your models here.
from .models import Profile
class ProfileAdmin(admin.ModelAdmin):
        #To display the list of items like  user,date_of_birth and photo
        list_display = ['user', 'date_of_birth', 'photo']
        #Register Profile ,ProfileAdmin
admin.site.register(Profile,ProfileAdmin)
