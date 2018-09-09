from django.contrib import admin
from .models import AREA,ORDER,ORDER_DETAIL,TABLE,TABLE_STATUS,SHOP,MENU

admin.site.register(AREA)
admin.site.register(SHOP)
admin.site.register(MENU)
admin.site.register(TABLE)
admin.site.register(TABLE_STATUS)
admin.site.register(ORDER)
admin.site.register(ORDER_DETAIL)
