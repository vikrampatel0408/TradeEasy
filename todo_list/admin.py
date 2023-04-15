from django.contrib import admin
from todo_list.models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(List)
admin.site.register(Stock)
admin.site.register(Contact)
admin.site.register(crypto_tbl)