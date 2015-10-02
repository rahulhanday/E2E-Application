from django.contrib import admin
from .models import Details, GlobalConfig

class DetailsAdmin(admin.ModelAdmin):

    """
        ModelAdmin for user Details
    """
    list_display = ['user', 'father_name', 'mother_name', 'city']

admin.site.register(Details, DetailsAdmin)


class GlobalConfigAdmin(admin.ModelAdmin):

    """
        ModelAdmin for class GlobalConfig
    """
    fields = ["name", "value"]
    list_display = ["name", "value"]

admin.site.register(GlobalConfig, GlobalConfigAdmin)