from django.contrib import admin

from django.contrib import admin
from .models import *


@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name')
    search_fields = ('serial_number', 'name')


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('designation', 'verbose_name')
    search_fields = ('designation', 'verbose_name')


@admin.register(SoftwareVersion)
class SoftwareVersionAdmin(admin.ModelAdmin):
    list_display = ('component', 'version', 'is_critical', 'is_broken', 'tractor_model', 'engine_comp',
                    'first_number', 'second_number', 'third_number')
    list_filter = ('is_critical', 'component')
    search_fields = ('component__designation',
                     'component__verbose_name')


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = ('tractor', 'component', 'software_version')
    list_filter = ('tractor', 'software_version')
    search_fields = ('tractor__serial_number', 'tractor__name')


