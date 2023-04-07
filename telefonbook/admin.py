from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Persone, Phone, Record, Importance


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1


class ModelInline(admin.StackedInline):
    model = Phone
    extra = 1


def delete(obj):
    view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
    link = reverse(view_name, args=[obj.pk])
    html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
    return format_html(html)


def change(obj):
    view_name = "admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name)
    link = reverse(view_name, args=[obj.pk])
    html = '<input type="button" onclick="location.href=\'{}\'" value="Edit" />'.format(link)
    return format_html(html)


@admin.register(Persone)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("id", "name", delete, change)
    fieldsets = [
        (None, {"fields": ["name"]})
    ]
    inlines = [PhoneInline]


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    search_fields = ("phone", "description")
    list_display = ("id", "phone", delete, change)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = ("id", "name", "description", "colors", "user", delete, change)
    list_filter = ("colors", "user")


@admin.register(Importance)
class ImportanceAdmin(admin.ModelAdmin):
    search_fields = ("color", "description")
    list_display = ("id", "color", "description", delete, change)


