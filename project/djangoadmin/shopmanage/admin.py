from django.contrib import admin
from .models import Users, Items, Purchases


class AdminDate(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', ]


admin.site.register(Users, AdminDate)
admin.site.register(Items, AdminDate)
admin.site.register(Purchases, AdminDate)
