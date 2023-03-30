from django.contrib import admin
from todo_list.models import Contact, List , T_List , crypto_tbl
from django.contrib.auth.admin import UserAdmin



admin.site.register(List)


admin.site.register(T_List)
admin.site.register(Contact)
admin.site.register(crypto_tbl)