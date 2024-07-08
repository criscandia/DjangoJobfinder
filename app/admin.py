from django.contrib import admin
from .models import RSSFeed

# Register your models here.


@admin.register(RSSFeed)
class RssFeedAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "site_name",
        "url",
        "last_fetched",
    )  # Mostrar estos campos en la lista de RSSFeed
    search_fields = (
        "title",
        "site_name",
    )  # Agregar un campo de búsqueda para estos campos
    list_filter = ("last_fetched",)  # Agregar un filtro para el campo last_fetched
