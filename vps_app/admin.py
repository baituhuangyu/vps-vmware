# -*- coding: utf-8 -*-
from django.contrib import admin


from vps_app.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

class UsrAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name','email']
    list_filter = ['user', 'user_name','email']
    list_editable = ['user', 'user_name','email']


class HostAdmin(admin.ModelAdmin):
    list_display = ['host_name', 'ip']
    list_filter = ['host_name', 'ip']
    list_editable = ['host_name', 'ip']


class VmAdmin(admin.ModelAdmin):
    list_display = ['name', 'vm_id']
    list_filter = ['name', 'vm_id']
    list_editable = ['name', 'vm_id']


class VmTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'vm_id']
    list_filter = ['name', 'vm_id']
    list_editable = ['name', 'vm_id']


admin.site.register(Usr, UsrAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Vm, VmAdmin)
admin.site.register(VmType, VmTypeAdmin)

