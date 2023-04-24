from django.contrib import admin

from core.models import PriceAlert

# Register your models here.
admin.site.register(PriceAlert)
admin.site.site_title = 'Amazon Price Checker'
admin.site.site_header = 'Amazon Price Checker Admin Panel'
