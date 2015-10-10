from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import Restaurant, SignUpForm, FormCustoms, Category, Order, Good, Menu, Custom, Department

admin.site.register(SignUpForm)
admin.site.register(FormCustoms)
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Good)
admin.site.register(Menu)
admin.site.register(Custom)
admin.site.register(Department)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CustomInline(admin.StackedInline):
    model = Custom
    can_delete = False
    verbose_name_plural = 'custom'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (CustomInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)