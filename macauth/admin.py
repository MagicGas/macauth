from django.contrib import admin
from macauth.models import User,MacAddr
# Register your models here.

# admin.site.register(User)
# admin.site.register(MacAddr)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display= ("username",)

@admin.register(MacAddr)
class MacAddrAdmin(admin.ModelAdmin):
    list_display= ("position","macaddr")